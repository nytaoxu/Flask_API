import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be blank."
    )

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items WHERE name=?"
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            if row:
                return {
                    "name": row[0],
                    "price": row[1]
                }
    
    @classmethod
    def insert(cls, item):
        try:
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                query = "INSERT INTO items VALUES (?, ?)"
                cursor.execute(query, (item["name"], item["price"]))
                connection.commit()
                return item
        except Exception as e:
            print(f"Exception in class mothod Item.insert(cls, item): {e}")

    @classmethod
    def update(cls, item):
        try:
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                query = "UPDATE items SET price=? WHERE name=?"
                cursor.execute(query, (item["price"], item["name"]))
                connection.commit()
                return item
        except Exception as e:
            print(f"Exception in class method Item.update(cls, item): {e}")

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {
            "message": f"Item with name {name} not found."
        }, 404
    

    def post(self, name):
        if Item.find_by_name(name):
            return {"message": f"The item with the name '{name}' already exists."}, 400
        
        data = Item.parser.parse_args()
        new_item = {
            "name": name,
            # "price": request.get_json()["price"]
            "price": data["price"]
        }
        try:
            Item.insert(new_item)
            return new_item, 201
        except Exception as e:
            print(f"Exception occurred inserting item: {e}")
            return {
                "message": f"Error occurred when posting: {e}"
            }, 500 # internal server error
    
    def delete(self, name):
        if not Item.find_by_name(name):
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
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        new_item = {
            "name": name,
            "price": data["price"]
        }
        if item:
            try:
                # with sqlite3.connect("data.db") as connection:
                #     cursor = connection.cursor()
                #     query = "UPDATE items SET price=? WHERE name=?"
                #     cursor.execute(query, (new_item["price"], name))
                #     connection.commit()
                Item.update(new_item)
                return new_item
            except Exception as e:
                print(f"Exception occurred when updating an item: {e}")
                return {
                    "message": f"Exception occurred when updating an item: {e}"
                }, 500
        else:
            try:
                Item.insert(new_item)
                return new_item, 201
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
