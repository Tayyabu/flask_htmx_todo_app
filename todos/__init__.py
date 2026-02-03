from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from sqlalchemy.orm import MappedAsDataclass
from flask_login import LoginManager
from flask import Flask
from flask_bcrypt import Bcrypt


class Base(MappedAsDataclass, DeclarativeBase):
    pass




db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = (
    "4a8d7f93cf7b64da6725c0cb8c0448d470c21d71e8769429bdb81414320d"
)
# initialize the app with the extension
login_manager.login_view = "login"  # type: ignore
login_manager.init_app(app)
db.init_app(app)
# SECRET_KEY

