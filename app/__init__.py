from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # MariaDB connection string using pymysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:@Nathi123@localhost/chickencoopdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
