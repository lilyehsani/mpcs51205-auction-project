# from flask import Flask,request, jsonify
# import os
# import json
# import sys
# sys.path.append('/Users/yunchenliu/Desktop/mpcs51205-auction-project/inventory')
# from accessor.category_accessor import CategoryAccessor
# from accessor.item_accessor import ItemAccessor
# from model.item import item_status

# # todo how to create table auto when starting the mysql-db service

# app = Flask(__name__)
# category_accessor = CategoryAccessor()
# item_accessor = ItemAccessor()

# err_msg = {
#     "param_err": "invalid param",
#     "db_err": "db error",
#     "service_err": "service error",
#     "not_found": "item not found in DB"
# }

# # -------- open APIs ----------
# @app.route('/')
# def home():
#     return "inventory index page"


# @app.route('/create_item',methods=['POST'])
# def create_item():
#     data = request.get_data()
#     data = json.loads(data)
#     check_result, error = check_item_input(data)
#     if not check_result:
#         return pack_err(error)
#     try:
#         item_id = item_accessor.create_item(data.get('name'), data.get('description'), data.get('quantity'), data.get('shipping_cost'), data.get('is_buy_now'), data.get('price'), item_status["normal"])
#         if item_id == -1:
#             return pack_err(err_msg["db_err"])
#         if not category_accessor.add_category_item_relation(item_id, data.get('category_id')):
#             return pack_err(err_msg["db_err"])
#     except Exception as e:
#         print("exception when creating item:", e)
#         return pack_err(err_msg["db_err"])
#     item_info = item_accessor.get_item_by_ids([item_id])
#     if not item_info or len(item_info) == 0:
#         return pack_err(err_msg["service_err"])
#     return pack_success(item_info)

# # http://10.1.1.1:5000/get_item?id=12345
# @app.route('/get_item',methods=['GET'])
# def get_item():
#     id = request.args.get('id')
#     item_info, err = get_item_by_id(id)
#     if not item_info:
#         return pack_err(err)
#     return pack_success(item_info)

# @app.route('/change_item_quantity',methods=['POST'])
# def change_item_quantity():
#     data = request.get_data()
#     data = json.loads(data)
#     id = data.get('id')
#     quantity = data.get('quantity')
#     query = {"id":id}
#     new_item = { "$set": {"quantity": quantity}}
#     try:
#         items.update_one(query, new_item)
#     except Exception as e:
#         print("change_item_cnt error", e)
#         return pack_err(err_msg["db_err"])
#     item_info, err = get_item_by_id(id)
#     if not item_info:
#         return pack_err(err)
#     return pack_success(item_info) 
    
# @app.route('/search_item', methods=['GET'])
# def get_all_categories():
#     pass

# @app.route('/update_item', methods=['POST'])
# def update_item():
#     pass

# @app.route('/delete_item', methods=['POST'])
# def delete_item():
#     pass

# @app.route('/red_flag_item', methods=['POST'])
# def red_flag_item():
#     pass

# @app.route('/add_category', methods=['POST'])
# def add_category():
#     pass

# @app.route('/update_category', methods=['POST'])
# def update_category():
#     pass

# @app.route('/delete_category', methods=['POST'])
# def delete_category():
#     pass

# @app.route('/get_items_by_category', methods=['POST'])
# def get_items_by_category():
#     pass

# @app.route('/get_all_categories', methods=['POST'])
# def get_all_categories():
#     pass

# # -------- inner functions ----------
# def get_item_by_id(id):
#     try:
#         ret_info= items.find_one({"id":id})
#     except Exception as e:
#         print("get_item_by_id error", e)
#         return None, err_msg["db_err"]
#     if not ret_info:
#         return None, err_msg["not_found"]
#     result = {
#         "name": ret_info['name'] if "name" in ret_info else "",
#         "id":ret_info['id'] if "id" in ret_info else "",
#         "description": ret_info['description'] if "description" in ret_info else "",
#         "quantity": ret_info['quantity'] if 'quantity' in ret_info else 0,
#         "shipping_cost": ret_info['shipping_cost'] if 'shipping_cost' in ret_info else 0,
#         "is_buy_now": ret_info['is_buy_now'] if 'is_buy_now' in ret_info else False,
#         "price": ret_info['price'] if 'price' in ret_info and 'is_buy_now' in ret_info and ret_info['is_buy_now'] else 0,
#         "status": ret_info['status'] if 'status' in ret_info else item_status["normal"],
#     }   
#     return result, ""

# def check_item_input(data):
#     try:
#         name = data.get('name')
#         assert name is not None, "invalid name"
#         assert isinstance(name, str), "invalid name"
#         description = data.get('description')
#         assert description is not None, "invalid description"
#         assert isinstance(description, str), "invalid description"
#         quantity = data.get('quantity')
#         assert quantity is not None, "invalid quantity"
#         assert isinstance(quantity, int), "invalid quantity"
#         shipping_cost = data.get('shipping_cost')
#         assert shipping_cost is not None, "invalid shipping_cost"
#         assert isinstance(shipping_cost, float) or isinstance(shipping_cost, int), "invalid shipping_cost"
#         is_buy_now = data.get('is_buy_now')
#         assert is_buy_now is not None, "invalid is_buy_now"
#         assert isinstance(is_buy_now, bool), "invalid is_buy_now"
#         price = data.get('price')
#         if is_buy_now == True:
#             assert price is not None, "invalid price"
#             assert isinstance(price, float) or isinstance(price, int), "invalid price"
#             assert price >= 0, "invalid price"
#         assert shipping_cost >= 0, "invalid shipping_cost"
#     except Exception as e:
#         print("create_item param error %s"%e)
#         return False, err_msg["param_err"]
#     return True, ""

# def pack_err(err_msg):
#     return jsonify({
#        "status":False,
#        "err_msg": err_msg
#     })

# def pack_success(data):
#     return jsonify({
#         "status": True,
#         "data": data
#     })

if __name__ == "__main__":
    print("xxx")
    # port = int(os.environ.get('PORT', 5000))
    # app.run(debug=True, host='0.0.0.0', port=port)