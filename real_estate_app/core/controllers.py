from flask import Blueprint, jsonify
from real_estate_app import app
from flask_restful import Api,Resource
from real_estate_app.products.models import Type,User,Product
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
core = Blueprint(__name__,'core')

api = Api(app)
ma = Marshmallow(app)

class ProductSchema(ModelSchema):
    class Meta:
        model = Product


class TypeSchema(ModelSchema):
    class Meta:
        model = Type

@core.route('/getproduct')
def getProduct():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({"products":output})

# api.add_resource(Types,"/types")

