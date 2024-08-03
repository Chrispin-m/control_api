from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL")

# API Key for authentication
API_KEY = os.getenv("API_KEY")

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to insert a new command into the database
def insert_command(phone_number, command):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO commands (phone_number, command)
    VALUES (%s, %s);
    """, (phone_number, command))
    conn.commit()
    cursor.close()
    conn.close()

# Endpoint to post a new command
@app.route('/post_command', methods=['POST'])
def post_command():
    if request.headers.get('API-KEY') != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    phone_number = data.get('phone_number')
    command = data.get('command')

    if not phone_number or not command:
        return jsonify({"error": "Phone number and command are required"}), 400

    insert_command(phone_number, command)
    return jsonify({"message": "Command inserted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
