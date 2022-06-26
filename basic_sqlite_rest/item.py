from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class ItemsList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        items = cursor.execute("SELECT * FROM items").fetchall()
        return items


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be empty'
                        )

    def get(self, name):
        item = self.find_item_by_name(name)
        if item:
            return item
        return {'meassgae': 'Item not found'}, 400

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        row = cursor.execute(query, (name,)).fetchone()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200

    def post(self, name):
        if self.find_item_by_name(name):
            return {'message': f"Item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message': 'Something went wrong'}, 500

        return item, 201

    @classmethod
    def insert_item(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"

        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE name=?", (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        try:
            if item is None:
                self.insert_item(updated_item)
            else:
                self.update_item(updated_item)
        except:
            return {'message': 'Something went wrong'}, 500
        return updated_item

    @classmethod
    def update_item(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price=? WHERE name=?",
                       (item['price'], item['name']))
        connection.commit()
        connection.close()
