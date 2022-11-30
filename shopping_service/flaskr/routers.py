from accessor.shopping_accessor import ShoppingAccessor
from accessor.db_init import DBInit
from common import err_msg
from model.item import item_status
from flask import Flask, request, jsonify
import os
from datetime import datetime
import json
import requests

app = Flask(__name__)
db_init = DBInit()
db_init.db_init()
shopping_accessor = ShoppingAccessor()
inventory_docker_url = 'http://inventory_service:5000'
inventory_local_url = 'http://localhost:5001'
inventory_url = inventory_docker_url

# ------------ open API --------------------
@app.route('/')
def home():
    return "shopping service home page"


# CreateItem
@app.route('/create_item', methods=['POST'])
def create_item():
    data = request.get_data()
    data = json.loads(data)
    user_id = data.get('user_id')
    # create item
    inventory_input = {'name': data.get('name'), 'description': data.get('description'), 'quantity' : data.get('quantity'), 'shipping_cost' :data.get('shipping_cost'), 'is_buy_now' : data.get('is_buy_now'), 'price' : data.get('price'), 'category_id': data.get('category_id')}
    inventory_input = json.dumps(inventory_input)
    r = requests.post(inventory_url + "/create_item", data=inventory_input)
    item, err = parse_response(r)
    if err:
        return pack_err(err)
    # create user_item info
    err = shopping_accessor.add_user_item(user_id=user_id, item_id=item['id'])
    if err:
        return pack_err(err)
    item['user_id'] = user_id 
    return pack_success(item)


# GetItemsForSaleByOwner
@app.route('/get_items_for_sale', methods=['GET'])
def get_items_for_sale():
    user_id = request.args.get('user_id')
    item_ids, err = shopping_accessor.get_items_by_user(user_id)
    if len(item_ids) == 0:
        return pack_success(None)
    if err:
        return pack_err(err)
    item_ids = [str(item_id[0]) for item_id in item_ids]
    item_id_input = "_".join(item_ids)
    r = requests.get(url=inventory_url + "/get_items?ids=" + item_id_input)
    items, err = parse_response(r)
    if err:
        return pack_err(err)
    ret_items = []
    for item in items:
        item['user_id'] = user_id 
        ret_items.append(item)   
    return pack_success(ret_items)


# RemoveItemForSale
@app.route('/remove_item_for_sale', methods=['POST'])
def remove_item_for_sale():
    data = request.get_data()
    data = json.loads(data)
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    try:
        shopping_accessor.remove_user_item(user_id=user_id, item_id=item_id)    
    except Exception as e:
        print(e)
        return pack_err(err_msg['db_err'])
    inventory_input = {
        'id':item_id
    }
    inventory_input = json.dumps(inventory_input)
    r = requests.post(inventory_url + "/delete_item", data=inventory_input)
    _, err = parse_response(r)
    if err:
        return pack_err(err)
    return pack_success(None)

# curl --location --request PUT 'http://127.0.0.1:5000/add_item_to_cart?id=1&item=1&quantity=1'
@app.route('/add_item_to_cart', methods=['PUT'])
def add_item_to_cart():
    user_id = request.args.get('id')
    item_id = request.args.get('item')
    quantity = request.args.get('quantity')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.add_item_to_cart(cart_id=cart_id, item_id=item_id, quantity=quantity)
    return pack_success(None)


# GetItemsInCartByUser
# curl --location --request GET 'http://127.0.0.1:5000/get_items_in_cart?id=1'
@app.route('/get_items_in_cart', methods=['GET'])
def get_items_in_cart():
    user_id = request.args.get('id')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    records = shopping_accessor.get_items_from_cart(cart_id=cart_id)
    if len(records) == 0:
        return pack_success(None)
    item_ids = [str(record[1]) for record in records]
    item_id_input = "_".join(item_ids)
    r = requests.get(url=inventory_url + "/get_items?ids=" + item_id_input)
    items, err = parse_response(r)  
    if err:
        return pack_err(err)  
    return pack_success(items)


# RemoveItemFromCart
# curl --location --request DELETE 'http://127.0.0.1:5000/remove_item_from_cart?id=1&item=1'
@app.route('/remove_item_from_cart', methods=['DELETE'])
def remove_item_from_cart():
    user_id = request.args.get('id')
    item_id = request.args.get('item')
    cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    shopping_accessor.remove_item_from_cart(cart_id=cart_id, item_id=item_id)
    return pack_success(None)


# Checkout
@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_data()
    data = json.loads(data)
    user_id = data.get('user_id')
    try:
        cart_id = shopping_accessor.get_current_cart(user_id=user_id)
    except Exception as e:
        print(e)
        return pack_err(err_msg['db_err'])
    try:
        items = shopping_accessor.get_items_from_cart(cart_id=cart_id)
        item_id_list, consume_quantity_list = [], []
        for item in items:
            item_id_list.append(int(item[1]))
            consume_quantity_list.append(int(item[2]))    
    except Exception as e:
        print(e)
        return pack_err(err_msg['db_err'])   
    inventory_input = {
        'id_list':item_id_list,
        'quantity_list':consume_quantity_list
    }
    inventory_input = json.dumps(inventory_input)
    r = requests.post(inventory_url + "/comsume_availble_items", data=inventory_input)
    result, err = parse_response(r)
    if err:
        return pack_err(err) 
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        shopping_accessor.checkout_items(cart_id, current_time)
    except Exception as e:
        print(e)
        return pack_err(err_msg['db_err'])
    return pack_success(result)    

# ---------------- inner function ------------------
def parse_response(resp):
    if resp.status_code != 200:
        return None, err_msg['micro_communication_err']
    try:
        data = json.loads(str(resp.text))
        if data['status'] != True:
            return None, data['err_msg']
        return data['data'], None
    except Exception as e:
        print(e)
        return None, err_msg['parse_err']


def pack_err(err_msg):
    return jsonify({
       "status":False,
       "err_msg": err_msg
    })


def pack_success(data):
    return jsonify({
        "status": True,
        "data": str(data)
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
