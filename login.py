from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from db import get_db_connection
import mysql.connector

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({"status": "failure", "message": "Username and password are required"}), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "failure", "message": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        # Fetch user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if user exists and password matches
        if user and check_password_hash(user['password'], password):
            return jsonify({"status": "success", "message": "Login successful"}), 200
        else:
            return jsonify({"status": "failure", "message": "Invalid username or password"}), 401
    except mysql.connector.Error as err:
        return jsonify({"status": "failure", "message": str(err)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
