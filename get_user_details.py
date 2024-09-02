from flask import Blueprint, request, jsonify
from db import get_db_connection
import mysql.connector

user_details_blueprint = Blueprint('user_details', __name__)

@user_details_blueprint.route('/user/<username>', methods=['GET'])
def get_user_details(username):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "failure", "message": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)

        # Fetch user details from the database by username
        cursor.execute("SELECT id, username, email, phone_number, profile_image, create_date_time, gender FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", "user": user}), 200
        else:
            return jsonify({"status": "failure", "message": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"status": "failure", "message": str(err)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
