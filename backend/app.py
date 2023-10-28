from flask import Flask, request, jsonify
from utils.sentiment_classification import get_sentiment
from flask_cors import CORS
import os
import psycopg
import bcrypt 

entry_id = 1
user_id = 1

app = Flask(__name__)
CORS(app)
conn = psycopg.connect(os.environ['DATABASE_URL'])

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT user_id, email, password_hash FROM users WHERE email = %s",
            (data['email'])
        )
        user_information = cursor.fetchone()

    if user_information is None:
        return 'Email or password is incorrect', 401
    
    if not bcrypt.checkpw(data['password'], user_information['password_hash']):
        return 'Email or password is incorrect', 401
    return 'Login successful', 200

@app.route('/register', methods=['POST'])
def register():
    global user_id
    data = request.json
    password_hash = bcrypt.hashpw(data['password'], bcrypt.gensalt())

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_information (user_id, email, password_hash) VALUES (%s, %s, %s)",
            (user_id, data['email'], password_hash)
        )
    user_id = user_id + 1
    conn.commit()
    return 200

@app.route('/store-entry', methods=['POST'])
def store_entry():
    global entry_id
    data = request.json
    current_timestamp = "CURRENT_TIMESTAMP"
    sentiment = get_sentiment(data['entry_text'])

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO diary_entries (entry_id, user_id, entry_time, entry_text, sentiment) VALUES (%s, %s, " + current_timestamp + ", %s, %s)",
            (entry_id, data['user_id'], data['entry_text'], sentiment)
        )

    entry_id = entry_id + 1

    conn.commit()
    return 200

@app.route('/get-entries', methods=['POST'])
def get_entries():
    data = request.json
    user_id = data['user_id']

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT entry_id, user_id, entry_time, sentiment, entry_text, sentiment FROM diary_entries WHERE user_id = %s",
            (user_id,)
        )
        entries = cursor.fetchall()

    keys = ['entry_id', 'user_id', 'entry_time', 'sentiment', 'entry_text', 'sentiment']
    entry_information = [{keys[i]: entry[i] for i in range(len(keys))} for entry in entries]

    return jsonify(entry_information)

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 3000
    app.run(host=HOST, port=PORT)