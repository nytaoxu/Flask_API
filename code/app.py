from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from datetime import timedelta

app = Flask(__name__)
PORT = 5000
# app.secert_key = "Tao"
app.config['SECRET_KEY'] = "Katherine"
# app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=10)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=PORT, debug=True)
