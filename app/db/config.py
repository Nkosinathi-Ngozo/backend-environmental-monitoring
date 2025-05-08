from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Nkosinathi:nathi123@localhost/chickencoopdb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Nkosinathi:@Nathi123@localhost/chickencoopdb'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
