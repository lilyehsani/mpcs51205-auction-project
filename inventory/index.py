from flask import Flask
import os
import pymongo 
import uuid

app = Flask(__name__)
dbclient = pymongo.MongoClient("mongodb://inventorydb:27017/")
db = dbclient["inventorydb"]
items = db["items"]

@app.route('/')
def home():
    create_item()
    result = items.count_documents({})
    return str(result)

def create_item(name, description, quantity, shipping_cost, is_buy_now, price):
    # todo param type check
    item_id = uuid.uuid1()
    item_list = [
        {"item_id": item_id, "name": name, "description": description, "quantity": quantity, "shipping_cost": shipping_cost, "is_buy_now": is_buy_now, "price": price, "status": 0},
    ]
    try:
        items.insert_many(item_list)
    except:
        return -1
    return item_id

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)