import json
from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'Sample Store',
        'items': [
            {
                'name': 'Sample Item',
                'price': 10
            }
        ]
    }
]


@app.route("/")
def hello():
    return "Store Rest API"


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>')
def get_store(name):
    filtered = [store for store in stores if store['name'] == name]
    if len(filtered) == 0:
        return jsonify({'message': 'Store not found'})
    return jsonify(stores[0])


@app.route('/store/<string:name>/item', methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    filtered = [store for store in stores if store['name'] == name]
    if len(filtered) == 0:
        return jsonify({'message': 'Store not found'})
    filtered[0]['items'].append(request_data['item'])
    return jsonify(filtered[0])


@ app.route('/store/<string:name>/item')
def get_store_items(name):
    filtered = [store for store in stores if store['name'] == name]
    if len(filtered) == 0:
        return jsonify({'message': 'Store not found'})
    return jsonify({'items': filtered[0]['items']})


if __name__ == '__main__':
    app.run(port=1234, debug=True)
