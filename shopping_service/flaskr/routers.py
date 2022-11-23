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

# CreateItemForSale
@app.route('/create_item/<user_id>', methods=['POST'])
def create_item(user_id):
    data = request.get_data()
    data = json.loads(data)
    # call inventory service
    r = requests.post("http://10.1.1.1:5000/create_item", data=data)
    # get item_id from response
    item_id = r.data
    shopping_accessor.add_user_item(user_id=user_id, item_id=item_id)


# AddItemToCart
# curl --location --request PUT 'http://127.0.0.1:5000/add_item_to_cart?id=1&item=1&quantity=1'
@app.route('/add_item_to_cart', methods=['PUT'])
def add_item_to_cart():
    user_id = request.args.get('id')
    item_id = request.args.get('item')
    quantity = request.args.get('quantity')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.add_item_to_cart(cart_id=cart_id, item_id=item_id, quantity=quantity)
    return pack_success(None)


# CheckoutItem
@app.route('/checkout/<user_id>', methods=['PUT'])
def checkout(user_id):
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shopping_accessor.checkout_items(cart_id, current_time)


# GetItemsForSaleByOwner
@app.route('/get_items_for_sale', methods=['GET'])
def get_items_for_sale():
    user_id = request.args.get('id')
    item_ids = shopping_accessor.get_items_for_sale_by_user(user_id=user_id)
    return pack_success(item_ids)


# GetItemsInCartByUser
@app.route('/get_items_in_cart', methods=['PUT'])
def get_items_in_cart():
    user_id = request.args.get('id')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    item_ids = shopping_accessor.get_items_from_cart(cart_id=cart_id)
    return pack_success(item_ids)


# RemoveItemFromCart
@app.route('/remove_item_from_cart', methods=['DELETE'])
def remove_item_from_cart():
    user_id = request.args.get('id')
    item_id = request.args.get('item')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.remove_item_from_cart(cart_id=cart_id, item_id=item_id)


def pack_success(data):
    return jsonify({
        "status": True,
        "data": data
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
