from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemsList

app = Flask(__name__)
app.secret_key = 'qwerty'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')
app.run(port=1234, debug=True)
