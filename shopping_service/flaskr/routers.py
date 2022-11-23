from accessor.shopping_accessor import ShoppingAccessor
from accessor.db_init import DBInit
from model.item import item_status
from flask import Flask, request, jsonify
import os
import datetime
import json
import requests

app = Flask(__name__)
db_init = DBInit()
db_init.db_init()
shopping_accessor = ShoppingAccessor()


@app.route('/')
def home():
    return "shopping service home page"


@app.route('/create_item/<user_id>', methods=['POST'])
def create_item(user_id):
    data = request.get_data()
    data = json.loads(data)
    # call inventory service
    r = requests.post("http://10.1.1.1:5000/create_item", data=data)
    # get item_id from response
    item_id = r.data
    shopping_accessor.add_user_item(user_id=user_id, item_id=item_id)


@app.route('/add_item_to_cart/<user_id>/<item_id>', methods=['PUT'])
def add_item_to_cart(user_id, item_id):
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.add_item_to_cart(cart_id=cart_id, item_id=item_id)


@app.route('/checkout/<user_id>', methods=['PUT'])
def checkout(user_id):
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shopping_accessor.checkout_items(cart_id, current_time)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)