from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
# app.secert_key = "jose"
app.config['SECRET_KEY'] = "jose"
# app.key_abc = "uvw"
api = Api(app)
jwt = JWT(app, authenticate, identity)

PORT = 5000
items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {
            "item": item
        }, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"The item with the name '{name}' already exists."}, 400
        data = Item.parser.parse_args()
        new_item = {
            "name": name,
            # "price": request.get_json()["price"]
            "price": data["price"]
        }
        items.append(new_item)
        return new_item, 201
    
    def delete(self, name):
        # for index, item in enumerate(items):
        #     if item["name"] == name:
        #         del(items[index])
        #         break
        # else:
        #     return {}, 404
        # return {}, 200
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item removed."}, 200
    
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item:
            # item["price"] = data["price"]
            item.update(data)
            return {
                "item": item
            }, 200
        else:
            item = {
                "name": name,
                "price": data["price"]
            }
            items.append(item)
            return {
                "item": item
            }, 201


class ItemList(Resource):
    def get(self):
        return {
            "items": items
        }, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=PORT, debug=True)
