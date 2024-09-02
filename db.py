import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',      # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'pypy'
}

# Helper function to connect to the database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Function to create tables if they do not exist
def create_tables():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            phone_number VARCHAR(15),
            profile_image VARCHAR(255),
            create_date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            gender ENUM('male', 'female', 'other') NOT NULL
        )
        """)
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()
        conn.close()
