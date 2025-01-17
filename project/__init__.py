# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_mail import Mail

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWfcahddvfvrtND4o83j4K4iuopOjerck8u4dnnc8iebs93gbao'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    app.config['MAIL_SERVER']='10.0.40.73'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = 'admin@sunpartners.local'
    app.config['MAIL_PASSWORD'] = 'Blueteam2022'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 512 # 512 MB

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()