from flask import Flask, request, jsonify
from utils.sentiment_classification import get_sentiment
from utils.chatbot import get_chatbot_response
from flask_cors import CORS
import os
import psycopg
from datetime import datetime

entry_id = 1
user_id = 1

app = Flask(__name__)
CORS(app)
conn = psycopg.connect(os.environ['DATABASE_URL'])

@app.route('/get-chat-response', methods=['POST'])
def get_chat_response():
    data = request.json
    context = data['context']
    def parse_context(context):
        parsed = ""
        for entry in context:
            parsed += f"you: {entry['chatbot']}, user: {entry['user']}, "
        return parsed[:-2] # remove the last comma and space
    try:
        formatted_context = parse_context(context)
    except:
        return 'Malformed input.', 400
    chatbot_response = get_chatbot_response(formatted_context)

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

    return 'Login successful.', 200

@app.route('/register', methods=['POST'])
def register():
    global user_id
    data = request.json


    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM user_information WHERE email = %s", (data['email'],))
        existing_user = cursor.fetchone()

    if existing_user:
        return "User already registered.", 400

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_information (user_id, email, user_password) VALUES (%s, %s, %s)",
            (user_id, data['email'], data['password'])
        )
    user_id = user_id + 1
    conn.commit()
    return 'User registered.', 200

@app.route('/store-entry', methods=['POST'])
async def store_entry():
    global entry_id
    data = request.json
    sentiment = await get_sentiment(data['entry_text'])

    current_date = datetime.now()
    formatted_date = current_date.strftime("%m/%d/%Y")

    with conn.cursor() as cursor:

        cursor.execute(
            "INSERT INTO diary_entries (entry_id, user_id, entry_date, entry_text, sentiment) VALUES (%s, %s, %s, %s, %s)",
            (entry_id, data['user_id'], formatted_date, data['entry_text'], sentiment)
        )

    entry_id = entry_id + 1

    conn.commit()
    return 'Entry stored.', 200

@app.route('/get-entries', methods=['POST'])
def get_entries():
    data = request.json
    user_id = data['user_id']

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