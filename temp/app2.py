from flask import Flask, jsonify, request, render_template
import json

stores = [
    {
        "store_name": "myStore",
        "items": [
            {
                "name": "Banana",
                "price": 17.69
            },
            {
                "name": "Chocolate",
                "price": 27.99
            }
        ]
    }
]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    # print(f"request = {request.data}")
    # print(dir(request))
    # content = json.loads(request.data)
    content = request.get_json()
    # print(f"content = {content}")
    new_store = {
        "store_name": content["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store["store_name"] == name:
            return jsonify(store)
    return jsonify({})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({"stores": stores})


# POST /store/<stirng:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    content = request.get_json()
    for index, store in enumerate(stores):
        if store["store_name"] == name:
            all_items = store["items"]
            all_items.append({
                "name": content["name"],
                "price": content["price"]
            })
            stores[index] = {
                "store_name": name,
                "items": all_items
            }
            return jsonify({
                "name": content["name"],
                "price": content["price"]
            })
    new_item = {
        "name": content["name"],
        "price": content["price"]
    }
    new_store = {
        "store_name": name,
        "items": [new_item]
    }
    stores.append(new_store)
    return jsonify({
        "message": "store created",
        "store": {
            "store_name": name,
            "items": [new_item]
        }
    })


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_store_items(name):
    for store in stores:
        if name == store["store_name"]:
            return jsonify({
                "items": store["items"]
            })
    return jsonify({
        "items": []
    })


app.run(port=5000)
