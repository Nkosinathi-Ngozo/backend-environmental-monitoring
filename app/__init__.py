from flask import Flask
from app.db.config import init_db  # <-- import initializer
from app.routes.authroutes import auth
from app.routes.roleroutes import role

def create_app():
    app = Flask(__name__)

    init_db(app)  # Initialize DB with config

    app.register_blueprint(auth)
    app.register_blueprint(role)

    return app
