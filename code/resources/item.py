import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {
            "message": f"Item with name {name} not found."
        }, 404
    

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"The item with the name '{name}' already exists."}, 400
        
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data["price"])
        try:
            new_item.insert()
            return new_item.json(), 201
        except Exception as e:
            print(f"Exception occurred inserting item: {e}")
            return {
                "message": f"Error occurred when posting: {e}"
            }, 500 # internal server error
    
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {
                "message": f"Item with the name '{name}' not found."
            }, 404
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
        return {"message": "item removed."}, 200
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, data["price"])
        if item:
            try:
                new_item.update()
                return new_item.json()
            except Exception as e:
                print(f"Exception occurred when updating an item: {e}")
                return {
                    "message": f"Exception occurred when updating an item: {e}"
                }, 500
        else:
            try:
                new_item.insert()
                return new_item.json(), 201
            except Exception as e:
                print(f"Exception occurred when inserting an item: {e}")
                return {
                    "message": f"Exception occurred when inserting an item: {e}"
                }, 500


class ItemList(Resource):
    def get(self):
        try:
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM items"
                cursor.execute(query)
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "name": row[0],
                        "price": row[1]
                    })
            return {
                "items": items
            }, 200
        except Exception as e:
            print(f"Exception occurred listing items: {e}")
            return {
                "message": f"Error occurred listing items: {e}"
            }, 500
