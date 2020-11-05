from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path = '/home')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/real_estate_db'  #db-nin adini duzelt
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_DIRS =os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(app)

from real_estate_app.core.controllers import core
from real_estate_app.products.controllers import products


app.register_blueprint(core)
app.register_blueprint(products)


