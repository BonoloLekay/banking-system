from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "development-key"

    @app.route("/")
    def home():
        return "Banking System"

    return app