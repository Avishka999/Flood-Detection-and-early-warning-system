
import os
import sqlite3
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend')
CORS(app) 

# database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            country TEXT,
            region TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

#API Endpoint to Save User Data

@app.route('/save_details', methods=['POST'])
def save_details():
    try:
        # Get the data
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        country = data.get('country')
        region = data.get('region')

        # Connect to the database file
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Insert the new user's data into the 'users' table
        cursor.execute(
            "INSERT INTO users (name, email, country, region) VALUES (?, ?, ?, ?)",
            (name, email, country, region)
        )
        conn.commit()
        conn.close()
        
        # Send message back to the frontend
        return jsonify({"message": "Account details saved successfully!"}), 200

    except sqlite3.IntegrityError:
        return jsonify({"error": "This email address is already registered."}), 409
    except Exception as e:
        print(f"Error saving to database: {e}")
        return jsonify({"error": "Could not save details to the database."}), 500

#Routes to Serve Frontend Files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)



