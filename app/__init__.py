from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    template_dir = os.path.join(root_dir, "templates")
    static_dir = os.path.join(root_dir, "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = "randomsecretkey"

    from .routes import main
    app.register_blueprint(main)

    return app