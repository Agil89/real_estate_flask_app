from flask import Blueprint

core = Blueprint(__name__,'core')

@core.route('/')
def home():
    return 'hello'