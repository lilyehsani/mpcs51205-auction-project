from struct import pack
from unicodedata import category
from flask import Flask,request, jsonify
import os
import json
from accessor.category_accessor import CategoryAccessor
from accessor.item_accessor import ItemAccessor
from accessor.db_init import DBInit
from model.item import item_status
from common import err_msg
from flask_cors import CORS

app = Flask(__name__)
db_init = DBInit()
db_init.db_init()
category_accessor = CategoryAccessor()
item_accessor = ItemAccessor()

# -------- open APIs ----------
@app.route('/')
def home():
    return "new inventory index page"

@app.route('/create_item',methods=['POST'])
def create_item():
    data = request.get_data()
    data = json.loads(data)
    check_result, error = check_item_input(data)
    if not check_result:
        return pack_err(error)
    item_id, err = item_accessor.create_item(data.get('name'), data.get('description'), data.get('quantity'), data.get('shipping_cost'), data.get('is_buy_now'), data.get('price'), item_status["normal"])
    if err:
        return pack_err("create item itself failed " + err)
    _, err = category_accessor.add_category_item_relation(int(item_id), int(data.get('category_id')))
    if err:
        return pack_err("link item to category failed " + err)
    item_info, err = item_accessor.get_item_by_ids([int(item_id)])
    if err:
        return pack_err(err)
    return pack_success(item_info[0].serialize())

# http://10.1.1.1:5000/get_item?id=12345
# http://10.1.1.1:5000/get_item?id=12345,23456
@app.route('/get_items',methods=['GET'])
def get_items():
    ids = request.args.get('ids')
    id_list = ids.split(",")
    items, err = item_accessor.get_item_by_ids(id_list)
    if err:
        return pack_err(err)    
    return pack_success([item.serialize() for item in items])

# id_list, list of item ids to consume
# quantity_list how many quantity want to be consumed for each item, pair with id_list
@app.route('/comsume_availble_items',methods=['POST'])
def comsume_availble_items():
    data = request.get_data()
    data = json.loads(data)
    id_list = data.get('id_list')
    quantity_list = data.get('quantity_list')
    if len(id_list) != len(quantity_list):
        return pack_err(err_msg['param_err'])
    items, err = item_accessor.get_item_by_ids(id_list)
    availble_item_to_quantity = {}
    result = {}
    for item in items:
        availble_item_to_quantity[item.id] = item.quantity
    for i in range(len(id_list)):
        cur_id = id_list[i]
        to_consume_quantity = quantity_list[i]
        avaible_quantity = availble_item_to_quantity[cur_id] if cur_id in availble_item_to_quantity else 0
        left_quantity = max(0, avaible_quantity - to_consume_quantity)
        _, err =  item_accessor.update_item_quantity(cur_id, left_quantity)
        if err:
            return pack_err(err)
        result[cur_id] = {
            "id": cur_id,
            "to_consume_quantity": quantity_list[i],
            "availble_item_to_quantity": availble_item_to_quantity[cur_id],
            "consumed_quantity" : min(to_consume_quantity, avaible_quantity),
            "left_quantity": left_quantity
        }
    return pack_success(result)        

@app.route('/update_item', methods=['POST'])
def update_item():
    data = request.get_data()
    data = json.loads(data)
    id = data.get('id')
    _, err = item_accessor.update_item(id, data.get('name'), data.get('description'), data.get('quantity'), data.get('shipping_cost'), data.get('is_buy_now'), data.get('price'), item_status["normal"])
    if err:
        return pack_err("update_item failed" + err)
    item_info, err = item_accessor.get_item_by_ids([id])
    if err:
        return pack_err(err)
    return pack_success(item_info[0].serialize()) 

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.get_data()
    data = json.loads(data)
    _, err = item_accessor.change_item_status(data.get('id'),  item_status["deleted"])
    if err:
        return pack_err("delete_item failed" + err)
    return pack_success(None)     

@app.route('/red_flag_item', methods=['POST'])
def red_flag_item():
    data = request.get_data()
    data = json.loads(data)
    _, err = item_accessor.change_item_status(data.get('id'),  item_status["red_flag"])
    if err:
        return pack_err("red_flag_item failed" + err)
    return pack_success(None)   
    
@app.route('/search_item', methods=['GET'])
def search_item():
    key_word = request.args.get('keyword')
    items, err = item_accessor.search_item_by_key_words(key_word)
    if err:
        return pack_err(err)
    return pack_success([item.serialize() for item in items])

@app.route('/create_category', methods=['POST'])
def add_category():
    data = request.get_data()
    data = json.loads(data)
    id, err = category_accessor.create_category(data.get('name'))    
    if err:
        return pack_err(err)
    category_info, err = category_accessor.get_category_by_ids([id])
    if err or len(category_info) == 0:
        return pack_err(err)
    return pack_success(category_info[0].serialize())

@app.route('/update_category', methods=['POST'])
def update_category():
    data = request.get_data()
    data = json.loads(data)
    id = data.get('id')
    _, err = category_accessor.update_category(id, data.get('name'))    
    if err:
        return pack_err(err)
    category_info, err = category_accessor.get_category_by_ids([id])
    if err or len(category_info) == 0:
        return pack_err(err)
    return pack_success(category_info[0].serialize())

@app.route('/delete_category', methods=['POST'])
def delete_category():
    data = request.get_data()
    data = json.loads(data)
    id = data.get('id')
    _, err = category_accessor.delete_category(int(id))
    if err:
        return pack_err(err)
    return pack_success(None)

@app.route('/get_items_by_category', methods=['GET'])
def get_items_by_category():
    id = request.args.get('id')
    items, err = item_accessor.search_item_by_category(int(id))
    if err:
        return pack_err(err)
    return pack_success([item.serialize() for item in items])  

@app.route('/get_all_categories', methods=['GET'])
def get_all_categories():
    categories, err = category_accessor.get_all_categories()
    if err:
        return pack_err(err)
    return pack_success([category.serialize() for category in categories])

@app.route('/get_red_flag_item',methods=['GET'])
def get_red_flag_item():
    items, err = item_accessor.get_red_flag_items()
    if err:
        return pack_err(err)
    return pack_success([item.serialize() for item in items])

# -------- inner functions ----------
def check_item_input(data):
    try:
        name = data.get('name')
        assert name is not None, "invalid name"
        assert isinstance(name, str), "invalid name"
        description = data.get('description')
        assert description is not None, "invalid description"
        assert isinstance(description, str), "invalid description"
        quantity = data.get('quantity')
        assert quantity is not None, "invalid quantity"
        assert isinstance(quantity, int), "invalid quantity"
        shipping_cost = data.get('shipping_cost')
        assert shipping_cost is not None, "invalid shipping_cost"
        assert isinstance(shipping_cost, float) or isinstance(shipping_cost, int), "invalid shipping_cost"
        is_buy_now = data.get('is_buy_now')
        assert is_buy_now is not None, "invalid is_buy_now"
        assert isinstance(is_buy_now, bool), "invalid is_buy_now"
        price = data.get('price')
        if is_buy_now == True:
            assert price is not None, "invalid price"
            assert isinstance(price, float) or isinstance(price, int), "invalid price"
            assert price >= 0, "invalid price"
        assert shipping_cost >= 0, "invalid shipping_cost"
    except Exception as e:
        print("create_item param error %s"%e)
        return False, err_msg["param_err"]
    return True, ""

def pack_err(err_msg):
    return jsonify({
       "status":False,
       "err_msg": err_msg
    })

def pack_success(data):
    return jsonify({
        "status": True,
        "data": data
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app)
    app.config['SECRET_KEY'] = 'super-secret'
    app.run(debug=True, host='0.0.0.0', port=port)