from flask import Flask,send_from_directory,session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import LoginManager,current_user




app = Flask(__name__,static_url_path = '/home')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@db:3306/real_estate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

BASE_DIRS =os.path.dirname(os.path.abspath(__file__))

UPLOADED_FILES_DIR = os.path.join(BASE_DIRS,'media')

MEDIA_URL = 'media'

if not os.path.isdir(UPLOADED_FILES_DIR):
    os.mkdir(UPLOADED_FILES_DIR)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADED_FILES_DIR,filename)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'real_estate_app.products.controllers.sign_in'



class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            user=User.query.filter_by(id=session.get("user_id")).first().is_superuser
            return user
        else:
            return False


admin = Admin(app)

from real_estate_app.products.models import Product,Type,City,Status,User,Images

admin.add_view((MyModelView(Product,db.session)))
admin.add_view((MyModelView(Type,db.session)))
admin.add_view((MyModelView(City,db.session)))
admin.add_view((MyModelView(Status,db.session)))
admin.add_view((MyModelView(User,db.session)))
admin.add_view((MyModelView(Images,db.session)))

migrate = Migrate(app, db)

from real_estate_app.core.controllers import core
from real_estate_app.products.controllers import products


app.register_blueprint(core)
app.register_blueprint(products)


