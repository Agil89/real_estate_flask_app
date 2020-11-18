from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,ValidationError,TextAreaField,IntegerField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length, Email
# from blog.auth.models import check_username,check_email
from real_estate_app.products.models import User,City,Type,Status
from real_estate_app import db
from flask_wtf.file import FileField,FileRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy.sql import func



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(2, 40), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=40), DataRequired()])

    def validate_username(self,field):
        exists = db.session.query(db.exists().where(User.username == field.data)).scalar()
        if not exists:
            raise ValidationError('Wrong username')
        return field

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[Length(2,40),DataRequired()])
    email = StringField('Email', validators=[Email(),Length(max=40), DataRequired()])
    first_name = StringField('Firstname', validators=[Length(max=40), DataRequired()])
    last_name = StringField('Lastname', validators=[Length(max=40), DataRequired()])
    phone_number = StringField('Phone number',validators=[Length(max=10), DataRequired()])
    password = PasswordField('Password',validators=[Length(min=8,max=40),DataRequired()])

    def validate_username(self,field):
        exists = db.session.query(db.exists().where(User.username == field.data)).scalar()
        if exists:
            raise ValidationError('Username already taken')
        return field
    def validate_email(self,field):
        exists = db.session.query(db.exists().where(User.email == field.data)).scalar()
        if exists:
            raise ValidationError('Email already taken')
        return field


    def validate_password(self,field):
        cap_letter = [letter for letter in field.data if 65 <= ord(letter) <=90]
        if field.data.isdigit():
            raise ValidationError('Enter at least one the letter.')
        elif not cap_letter:
            raise ValidationError('Type at least one title letter.')
        return field


def city_choice():
    return City.query

def status_choice():
    return Status.query

def type_choice():
    return Type.query

class RegisterProduct(FlaskForm):
    title = StringField('Title',validators=[Length(2,40),DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[Length(max=100), DataRequired()])
    image = FileField(label='Image',validators=[FileRequired()])
    price = IntegerField('Price')
    is_published = BooleanField('Is active')
    city_id=QuerySelectField('City',query_factory=city_choice)
    type_id=QuerySelectField('Type',query_factory=type_choice)
    status_id = QuerySelectField('Status',query_factory=status_choice)


