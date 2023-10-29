from flask import Flask, request, jsonify
from utils.sentiment_classification import get_sentiment
from utils.chatbot import get_chatbot_response
from flask_cors import CORS
import os
import psycopg
from datetime import datetime

app = Flask(__name__)
CORS(app)
conn = psycopg.connect(os.environ['DATABASE_URL'])

@app.route('/get-chat-response', methods=['POST'])
def get_chat_response():
    data = request.json
    context = data['context']
    try:
        chatbot_response = get_chat_response(context)
    except KeyError:
        return 'Malformed input.', 400

    return chatbot_response, 200

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
    if 'entry_text' not in data:
        return 'Malformed input.', 400
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (user_id) FROM user_information WHERE user_id = %s",
            (data['user_id'],)
        )
        user_information = cursor.fetchone()
    if user_information is None:
        return 'User does not exist.', 400

    sentiment = await get_sentiment(data['entry_text'])

    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")

    with conn.cursor() as cursor:

        cursor.execute(
            "INSERT INTO diary_entries (user_id, entry_date, entry_text, sentiment) VALUES (%s, %s, %s, %s)",
            (data['user_id'], formatted_date, data['entry_text'], sentiment)
        )

    conn.commit()
    return 'Entry stored.', 200

@app.route('/get-entries', methods=['POST'])
def get_entries():
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

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT (entry_id, user_id, entry_date, sentiment, entry_text) FROM diary_entries WHERE user_id = %s",
            (user_id,)
        )
        entries = cursor.fetchall()

    keys = ['entry_id', 'user_id', 'entry_date', 'sentiment', 'entry_text']
    entry_information = [{keys[i]: entry[0][i] for i in range(len(keys))} for entry in entries]

    return jsonify(entry_information), 200

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 3000
    app.run(host=HOST, port=PORT, debug=True)