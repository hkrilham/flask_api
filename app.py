from flask import Flask
from db import create_tables
from signup import signup_blueprint
from login import login_blueprint
from get_user_details import user_details_blueprint

# Initialize the Flask application
app = Flask(__name__)

# Register blueprints or routes
app.register_blueprint(signup_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_details_blueprint)

if __name__ == '__main__':
    create_tables()  # Automatically create tables if they don't exist
    app.run(debug=True)
