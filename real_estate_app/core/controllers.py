from flask import Blueprint, jsonify,request
from real_estate_app import app
from flask_restful import Api,Resource
from real_estate_app.products.models import Type,User,Product,Status,City
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

# @core.route('/getproducts')
# def getProduct():
#     products = Product.query.all()
#     product_schema = ProductSchema(many=True)
#     output = product_schema.dump(products)
#     return jsonify({"products":output})

# api.add_resource(Types,"/types")
@core.route('/getproduct')
def getAll():
    minPrice = request.args.get('minPrice')
    maxPrice = request.args.get('maxPrice')
    products = Product.query.all()
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',type(products))
    # print(request.args.get('checked_types[]'))
    if maxPrice:
        for x in products:
            if int(x.price) >= int(maxPrice):
                products.remove(x)
    if minPrice:
        for x in products:
            if int(x.price) <= int(minPrice):
                products.remove(x)

    if request.args.get('checked_types[]'):
        type = Type.query.filter_by(title=request.args.get('checked_types[]')).first().id
        for x in products:
            if int(x.type_id) != int(type):
                products.remove(x)
        # products = products.filter(type_id=type).all()
    if request.args.get('checked_statuses[]'):
        status = Status.query.filter_by(title=request.args.get('checked_statuses[]')).first().id
        for x in products:
            if int(x.status_id) != int(status):
                products.remove(x)
                print(products)
    if request.args.get('selected_city'):
        city = City.query.filter_by(title=request.args.get('selected_city')).first().id
        for x in products:
            if int(x.city_id) != int(city):
                products.remove(x)
                print(products)
        # products = products.filter(status_id=status).all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({"products": output})
