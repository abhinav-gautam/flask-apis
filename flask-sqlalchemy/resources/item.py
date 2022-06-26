from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemsList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be empty'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item requires a store_id'
                        )

    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'meassgae': 'Item not found'}, 400

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': f"Item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        print(item)
        try:
            item.save_to_db()
        except:
            return {'message': 'Something went wrong'}, 500
        print('saved to db')

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        try:
            if item is None:
                item = ItemModel(name,**data)
            else:
                item.price = data['price']
                item.store_id = data['store_id']
            item.save_to_db()
        except:
            return {'message': 'Something went wrong'}, 500
        return item.json()

  