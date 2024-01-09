from flask import Flask
from flask_ckeditor import CKEditor

from peewee import SqliteDatabase

db = SqliteDatabase('database.db')
ckeditor = CKEditor()

def create_app():
    from .views import views
    from .auth import auth
    from .images import images
    from .models import User, Article

    db.create_tables((User, Article))

    app = Flask(__name__)
    app.secret_key = "oBiQmeKH9URLPoGUf5e4juFdUWxMYZoLeCg3BHqfarJzj2BUKa"

    ckeditor.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(images, url_prefix='/images')

    return app
