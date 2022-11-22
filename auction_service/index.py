from flask import Flask, request, jsonify
from flaskr.accessor.auction_accessor import AuctionAccessor
from datetime import datetime
import os
import json

app = Flask(__name__)

# -------- open APIs ----------
@app.route("/")
def home():
    return "auction index page"

@app.route("/create_auction",methods=["POST"])
def create_auction():
    data = request.get_data()
    data = json.loads(data)
    print(data)
    check_result, err = check_auction_input(data)
    if not check_result:
        print(err)
        # return pack_err(err)
    accessor = AuctionAccessor()
    try:
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        auction_id = accessor.create_new_auction(start_time, end_time, data.get("quantity"), data.get("item_id"))
        print(auction_id)
    except Exception as err:
        print(err)
        return jsonify({
            "status": False,
            "err_msg": str(err)
            })
        # return pack_err("An exception occurred")
    try:
        auction_info = accessor.get_auction_by_id(auction_id)
        print(auction_info)
    except Exception as err:
        print(err)
        return
        # return pack_err("An exception occurred")
    return pack_success(auction_info.to_json())

@app.route("/get_all_auction",methods=["GET"])
def get_all_auction():
    accessor = AuctionAccessor()
    try:
        auctions = accessor.get_all_auction()
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    json_auctions = []
    for auction in auctions:
        json_auctions.append(auction.to_json())
    return pack_success(json_auctions)

@app.route("/get_auction",methods=["GET"])
def get_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")
    try:
        auction_info = accessor.get_auction_by_id(auction_id)
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    return pack_success(auction_info.to_json())

@app.route("/start_auction",methods=["POST"])
def start_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")
    try:
        accessor.update_auction(auction_id, "status", 1)
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    return json_success()

@app.route("/end_auction_by_time",methods=["POST"])
def end_auction_by_time():
    # TODO: call shopping API and place item in user's cart
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")
    try:
        accessor.update_auction(auction_id, "status", 2)
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    return json_success()

@app.route("/end_auction_by_purchase",methods=["POST"])
def end_auction_by_purchase():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")
    try:
        accessor.update_auction(auction_id, "status", 3)
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    return json_success()

@app.route("/cancel_auction",methods=["POST"])
def cancel_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")
    try:
        accessor.update_auction(auction_id, "status", 4)
    except Exception as err:
        print(err)
        return
        # return pack_err(err)
    return json_success()

# -------- inner functions ----------
def check_auction_input(data):
    try:
        start_time = data.get("start_time")
        assert start_time is not None, "invalid start time"
        assert isinstance(start_time, str), "invalid start time"
        end_time = data.get("end_time")
        assert end_time is not None, "invalid end time"
        assert isinstance(end_time, str), "invalid end time"
        quantity = data.get("quantity")
        assert quantity is not None, "invalid quantity"
        assert isinstance(quantity, int), "invalid quantity"
        item_id = data.get("item_id")
        assert item_id is not None, "invalid item id"
        assert isinstance(item_id, int), "invalid item id"
    except Exception as e:
        print("create_item param error %s"%e)
        return False, "Invalid Parameter"
    return True, ""

def pack_err(err_msg):
    return jsonify({
       "status": False,
       "err_msg": err_msg
    })

def pack_success(data):
    return jsonify({
        "status": True,
        "data": data
    })

def json_success():
    return jsonify({
        "status": True
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, host="0.0.0.0", port=port)