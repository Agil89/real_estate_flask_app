from real_estate_app import db,login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from sqlalchemy_utils import PhoneNumber


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    created_at= db.Column(db.DateTime(timezone=True),server_default=func.now())
    is_published = db.Column(db.Boolean(), default=True, nullable=False)
    images = db.relationship("Images", backref="product")

    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    city_id=db.Column(db.Integer(),db.ForeignKey('city.id'))
    type_id=db.Column(db.Integer(),db.ForeignKey('type.id'))
    status_id = db.Column(db.Integer(), db.ForeignKey('status.id'))

    def __repr__(self):
        return self.title

    def getcity(self):
        return self.city.title()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),nullable=False)
    email = db.Column(db.String(40),nullable=False)
    first_name = db.Column(db.String(40),nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    # phone_country_code = db.Column(db.Unicode(10))
    password_hash = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean(),default=True,nullable=False)
    is_superuser = db.Column(db.Boolean(),default=False,nullable=False)
    date_joined= db.Column(db.DateTime(timezone=True),server_default=func.now())

    products = db.relationship("Product",backref="user")

    # phone_number = db.composite(
    #     PhoneNumber,
    #     _phone_number,
    #     phone_country_code
    # )

    def __init__(self,username,email,first_name,last_name,phone_number,password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number=phone_number
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(40), nullable=False)

    products = db.relationship("Product", backref="city")

    def __repr__(self):
        return self.title

class Type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(40), nullable=False)

    products = db.relationship("Product", backref="type")

    def __repr__(self):
        return self.title


class Status(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(40), nullable=False)

    products = db.relationship("Product", backref="status")

    def __repr__(self):
        return self.title

class Images(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(500), nullable=False)

    product_id = db.Column(db.Integer(),db.ForeignKey('product.id'))




db.create_all()

