from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name, age = data.get('name'), data.get('age')
    
    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
    return jsonify({"message": "User added successfully"})

@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return jsonify(users)

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name, age = data.get('name'), data.get('age')
    
    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
        conn.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
