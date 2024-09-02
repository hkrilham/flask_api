from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from db import get_db_connection
from mysql.connector import errorcode

signup_blueprint = Blueprint('signup', __name__)

@signup_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    profile_image = data.get('profile_image')
    gender = data.get('gender')

    # Check for required fields
    if not username or not email or not password:
        return jsonify({"status": "failure", "message": "Username, email, and password are required"}), 400

    # Validate gender
    if gender not in ['male', 'female', 'other']:
        return jsonify({"status": "failure", "message": "Gender must be 'male', 'female', or 'other'"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "failure", "message": "Database connection failed"}), 500
        cursor = conn.cursor()

        # Insert the new user into the database
        cursor.execute(
            """
            INSERT INTO users (username, email, password, phone_number, profile_image, create_date_time, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (username, email, hashed_password, phone_number, profile_image, datetime.now(), gender)
        )
        conn.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        # Check for specific error codes, like duplicate entries
        if err.errno == errorcode.ER_DUP_ENTRY:
            return jsonify({"status": "failure", "message": "Username or email already exists"}), 409
        return jsonify({"status": "failure", "message": str(err)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
