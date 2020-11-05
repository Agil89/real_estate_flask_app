from flask import Blueprint
from real_estate_app.products import models
products = Blueprint(__name__,'products')

@products.route('/products')
def all_products():
    return 'products'