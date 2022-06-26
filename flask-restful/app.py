from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'qwerty'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class ItemsList(Resource):
    @jwt_required()
    def get(self):
        return items


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be empty'
                        )

    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 400

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': f"Item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
app.run(port=1234, debug=True)
