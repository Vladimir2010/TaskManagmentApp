from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os

app = Flask(__name__)
DB_NAME = "cloud_server.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        token TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        client_task_id INTEGER,
        title TEXT,
        status TEXT,
        due_date TEXT,
        cloud_id TEXT UNIQUE
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": "Registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
        # Simple token for demo
        token = f"token-{row[0]}" 
        return jsonify({"token": token, "user_id": row[0]}), 200
        
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/sync', methods=['POST'])
def sync():
    # Mock Sync Endpoint
    # Receives list of tasks, updates them, returns new state
    data = request.json
    return jsonify({"status": "synced", "server_time": "2024-01-01T12:00:00"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
