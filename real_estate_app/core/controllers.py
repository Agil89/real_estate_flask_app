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

    city = ma.Nested("CitySchema")


class TypeSchema(ModelSchema):
    class Meta:
        model = Type

class CitySchema(ModelSchema):
    class Meta:
        model = City



@core.route('/getproduct')
def getAll():
    minPrice = request.args.get('minPrice')
    maxPrice = request.args.get('maxPrice')
    products = Product.query.all()
    if maxPrice:
        l_max = []
        for x in products:
            if not int(x.price) >= int(maxPrice):
                l_max.append(x)
    else:
        l_max=products
    if minPrice:
        l_min = []
        for x in l_max:
            if not int(x.price) <= int(minPrice):
                l_min.append(x)
    else:
        l_min=l_max
    if request.args.get('checked_types[]'):
        l_types = []
        type = Type.query.filter_by(title=request.args.get('checked_types[]')).first().id
        for x in l_min:
            if int(x.type_id) == int(type):
                l_types.append(x)
    else:
        l_types=l_min
    if request.args.get('checked_statuses[]'):
        print(request.args.get('checked_statuses[]'))
        l_status=[]
        status = Status.query.filter_by(title=request.args.get('checked_statuses[]')).first().id
        for x in l_types:
            if int(x.status_id) == int(status):
                l_status.append(x)
    else:
        l_status = l_types
    if request.args.get('selected_city'):
        l_city=[]
        city = City.query.filter_by(title=request.args.get('selected_city')).first().id
        for x in l_status:
            if not int(x.city_id) != int(city):
                l_city.append(x)
    else:
        l_city = l_status
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(l_city)
    return jsonify({"products": output})

@core.route('/search')
def getproducts():
    search_word=request.args.get('inputValue')
    products=Product.query.filter(Product.description.contains(search_word)).all()
    print('asdfasfasdfasdfasdfasdgfasfdgafdsgadfgfdagdfgdsfgsdfgsdrfAAAAAAAAAAAAAAAA',products)
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({"products": output})