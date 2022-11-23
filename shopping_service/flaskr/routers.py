from accessor.shopping_accessor import ShoppingAccessor
from model.item import item_status
from flask import Flask, request, jsonify
import datetime
import requests
import json

app = Flask(__name__)
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
    shopping_accessor.update_user_item(user_id=user_id, item_id=item_id)


@app.route('/add_item_to_cart/<user_id>/<item_id>', methods=['PUT'])
def add_item_to_cart(user_id, item_id):
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.add_item_to_cart(cart_id=cart_id, item_id=item_id)


@app.route('/checkout/<user_id>', methods=['PUT'])
def checkout(user_id):
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shopping_accessor.checkout_items(cart_id, current_time)
