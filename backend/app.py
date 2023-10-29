from flask import Flask, request, jsonify
from utils.sentiment_classification import get_sentiments
from utils.chatbot import get_chatbot_response, get_weekly_summary, get_daily_summary
from utils.date_manipulation import get_first_day_of_week
from flask_cors import CORS
import os
import psycopg
from datetime import datetime

app = Flask(__name__)
CORS(app)
conn = psycopg.connect("postgresql://apai25:ZqZMx32nohbDmTaTwOqGZQ@mental-map-3658.g95.cockroachlabs.cloud:26257/defaultdb?sslmode=require")
EMOTIONS = ['Anger', 'Anxiety', 'Disappointment', 'Excitement', 'Fear', 'Joy', 'Love', 'Pain', 'Sadness', 'Tiredness']

@app.route('/get-chat-response', methods=['POST'])
def get_chat_response():
    data = request.json
    context = data['context']
    try:
        chatbot_response = get_chatbot_response(context)
    except KeyError:
        return 'Malformed input.', 400

    return jsonify({'chat_response': chatbot_response}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id, email, user_password) FROM user_information WHERE email = %s",
            (data['email'],)
        )
        user_information = cursor.fetchone()

    if user_information is None:
        return 'Email or password is incorrect.', 401

    if data['password'] != user_information[0][2]:
        return 'Email or password is incorrect.', 401

    return jsonify({'user_id': user_information[0][0]}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if 'email' not in data or 'password' not in data:
        return 'Malformed input.', 400

    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM user_information WHERE email = %s", (data['email'],))
        existing_user = cursor.fetchone()

    if existing_user:
        return "User already registered.", 400

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_information (email, user_password) VALUES (%s, %s)",
            (data['email'], data['password'])
        )
    conn.commit()

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id, email, user_password) FROM user_information WHERE email = %s",
            (data['email'],)
        )
        user_information = cursor.fetchone()
    
    return jsonify({'user_id': user_information[0][0]}), 200

@app.route('/store-entry', methods=['POST'])
async def store_entry():
    data = request.json
    if 'context' not in data:
        return 'Malformed input.', 400
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id) FROM user_information WHERE user_id = %s",
            (data['user_id'],)
        )
        user_information = cursor.fetchone()

    if user_information is None:
        return 'User does not exist.', 400

    entry_text = get_daily_summary(data['context'])
    sentiments = await get_sentiments(entry_text)

    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")

    with conn.cursor() as cursor:
        cursor.execute(
            "UPSERT INTO diary_entries (entry_id, user_id, entry_date, entry_text, anger, anxiety, disappointment, excitement, fear, joy, love, pain, sadness, tiredness) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['entry_id'], data['user_id'], formatted_date, entry_text, sentiments['Anger'], sentiments['Anxiety'], sentiments['Disappointment'], sentiments['Excitement'], sentiments['Fear'], sentiments['Joy'], sentiments['Love'], sentiments['Pain'], sentiments['Sadness'], sentiments['Tiredness'])
        )

    conn.commit()
    return 'Entry stored.', 200

@app.route('/get-entries', methods=['POST'])
def get_entries():
    data = request.json
    user_id = data['user_id']
    formatted_date = data['date']

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id) FROM user_information WHERE user_id = %s",
            (user_id,)
        )
        entries = cursor.fetchone()
    
    if entries is None:
        return 'User does not exist.', 400

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM diary_entries WHERE user_id = %s AND entry_date = %s",
            (user_id, formatted_date)
        )
        entries = cursor.fetchall()
    
    entry_information = []
    for entry in entries:
        emotion_vals = [(EMOTIONS[i], entry[i + 4]) for i in range(len(EMOTIONS))]
        emotion_vals.sort(key=lambda x: x[1], reverse=True)
        emotion_vals = emotion_vals[:3]
        
        sum_vals = sum([val[1] for val in emotion_vals])
        emotion_vals = [(val[0], val[1] * (100 / sum_vals)) for val in emotion_vals]
        
        entry_information.append({
            'entry_id': entry[0],
            'user_id': entry[1],
            'entry_date': entry[2],
            'entry_text': entry[3],
            'sentiments': emotion_vals,
        })

    return jsonify(entry_information), 200

@app.route('/get-weekly-summary', methods=['POST'])
async def get_weekly_entry_summary():
    data = request.json
    user_id = data['user_id']

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id) FROM user_information WHERE user_id = %s",
            (user_id,)
        )
        entries = cursor.fetchone()
    
    if entries is None:
        return 'User does not exist.', 400
    
    monday_date = get_first_day_of_week()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (entry_text) FROM diary_entries WHERE user_id = %s AND entry_date >= %s",
            (user_id, monday_date)
        )
        entries = cursor.fetchall()
    
    if not len(entries):
        return jsonify({'weekly_summary': 'No entries so far!', 'sentiments': [('Have a', 100), ('good', 100), ('week!', 100)]}), 200
    
    day_summaries = [entry[0][0] for entry in entries]
    weekly_summary = get_weekly_summary(day_summaries)
    sentiments = await get_sentiments(weekly_summary)
    sentiments = [(k, sentiments[k]) for k in sentiments]
    sentiments.sort(key=lambda x: x[1], reverse=True)
    sentiments = sentiments[:3]
    sum_sentiments = sum([sentiment[1] for sentiment in sentiments])
    sentiments = [(pair[0], pair[1] * (100 / sum_sentiments)) for pair in sentiments]

    return jsonify({'weekly_summary': weekly_summary, 'sentiments': sentiments}), 200

@app.route('/get-entry-dates', methods=['POST'])
def get_entry_dates():
    data = request.json

    if 'user_id' not in data:
        return 'Malformed input.', 400

    user_id = data['user_id']

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id) FROM user_information WHERE user_id = %s",
            (user_id,)
        )
        entries = cursor.fetchone()
    
    if entries is None:
        return 'User does not exist.', 400

    with conn.cursor() as cursor:
        cursor.execute('SELECT entry_date FROM diary_entries WHERE user_id = %s', (user_id, ))
        entries = cursor.fetchall()
    dates = list(set([entry[0] for entry in entries]))

    return dates, 200

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 3000
    app.run(host=HOST, port=PORT, debug=True)