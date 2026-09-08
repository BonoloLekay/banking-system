import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.database import get_connection
from app.routes.auth import auth_bp
from app.user import User


load_dotenv()

login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                user_id,
                customer_id,
                username,
                email,
                role,
                is_active
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        data = cursor.fetchone()

        if not data:
            return None

        return User(
            user_id=data["user_id"],
            customer_id=data["customer_id"],
            username=data["username"],
            email=data["email"],
            role=data["role"],
            is_active=data["is_active"]
        )

    finally:
        cursor.close()
        connection.close()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app