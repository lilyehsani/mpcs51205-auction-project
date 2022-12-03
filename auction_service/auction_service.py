from flask import Flask, request, jsonify
from flaskr.accessor.auction_accessor import AuctionAccessor
from flaskr.model.auction import auction_status
from datetime import datetime
import os
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
inventory_url = "http://inventory_service:5000/"
shopping_url = "http://shopping_service:5000/"
account_url = "http://account_service:5000/account/"
email_url = "http://email_service:5007/"

# -------- open APIs ----------
@app.route("/")
def home():
    return "auction routers page"

# Requires: start_time, end_time (timestamps in %Y-%m-%d %H:%M:%S format); 
# item_id (int), ID of item that has already been created in inventory service
@app.route("/create_auction",methods=["POST"])
def create_auction():
    data = request.get_data()
    data = json.loads(data)
    check_result, err = check_auction_input(data)
    if not check_result:
        return pack_err(str(err))

    accessor = AuctionAccessor()

    try:
        check_item = requests.get(inventory_url + "get_items?ids=" + str(data.get("item_id")))
    except Exception as err:
        return pack_err(str(err))
    
    check_item_success = check_success(check_item)
    if not check_item_success:
        return pack_err("Item does not exist.")

    try:
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        auction_id = accessor.create_new_auction(start_time, end_time, float(data.get("start_price")), data.get("item_id"))
    except Exception as err:
        return pack_err(str(err))

    try:
        auction_info = accessor.get_auction_by_id(auction_id)
    except Exception as err:
        return pack_err(str(err))
    return pack_success(auction_info.to_json())

# Requires: auction_id (int), ID of existing auction; user_id (str), ID of existing user (bidder); 
# bid_amount (int or float), amount of the bid being placed
@app.route("/place_bid",methods=["POST"])
def place_bid():
    # Get and check the input from the request
    data = request.get_data()
    data = json.loads(data)
    check_result, err = check_bid_input(data)
    if not check_result:
        return pack_err(str(err))

    # Create an auction accessor
    accessor = AuctionAccessor()
    auction_id = data.get("auction_id")

    # Get the auction being bid on
    try:
        auction = accessor.get_auction_by_id(auction_id)
    except Exception as err:
        return pack_err(str(err))
    
    # Get the current winning bid ID
    # Will be used later to notify the outbid user
    winning_bid_id = auction.current_highest_bid_id
    bid_amount = data.get("bid_amount")

    try:
        bid_time = datetime.now()
        accessor.place_bid(auction_id, data.get("user_id"), bid_amount, bid_time)
    except Exception as err:
        return pack_err(str(err))
        
    # Notify losing_user
    if winning_bid_id is not None:
        err = try_notify_bidder(accessor, winning_bid_id)
        if err:
            return pack_err(err)

    # Notify seller
    # item_id = auction.item_id

    # try:
    #     response = requests.get(inventory_url + "get_items?ids=" + item_id)
    # except Exception as err:
    #     return pack_err(str(err))
        
    # try:
    #     response = json.loads(response.text)
    # except json.decoder.JSONDecodeError as err:
    #     return pack_err(str(err))
        
    # subject = "Someone placed a bid!"
    # body = "Someone just placed a bid of ${} on your auction.".format(bid_amount)

    # try:
    #     response = requests.get(account_url + str(losing_user))
    # except Exception as err:
    #     return pack_err(str(err))

    # try:
    #     response = json.loads(response.text)
    # except json.decoder.JSONDecodeError as err:
    #     return pack_err(str(err))

    # losing_user_email = response.get("email")
    # post_data = {"subject": subject, "body": body, "to": losing_user_email}
    
    # # We should still allow bid even if email fails
    # requests.post(email_url + "send_email", json=post_data)

    # seller_id = response["data"][0].get("")

    return json_success()

# Requires: None
@app.route("/get_all_auction",methods=["GET"])
def get_all_auction():
    accessor = AuctionAccessor()

    try:
        auctions = accessor.get_all_auction()
    except Exception as err:
        return pack_err(str(err))

    json_auctions = []
    for auction in auctions:
        json_auctions.append(auction.to_json())

    return pack_success(json_auctions)

# Requires: None
@app.route("/get_all_startable_auction",methods=["GET"])
def get_all_startable_auction():
    accessor = AuctionAccessor()

    try:
        auctions = accessor.get_all_auction_by_status(auction_status["created"])
    except Exception as err:
        return pack_err(str(err))

    json_auctions = []
    for auction in auctions:
        json_auctions.append(auction.to_json())

    return pack_success(json_auctions)

# Requires: None
@app.route("/get_all_endable_auction",methods=["GET"])
def get_all_endable_auction():
    accessor = AuctionAccessor()

    try:
        auctions = accessor.get_all_auction_by_status(auction_status["online"])
    except Exception as err:
        return pack_err(str(err))

    json_auctions = []
    for auction in auctions:
        json_auctions.append(auction.to_json())

    return pack_success(json_auctions)

# Requires: id (int), ID of existing auction
@app.route("/get_auction",methods=["GET"])
def get_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        auction_info = accessor.get_auction_by_id(auction_id)
    except Exception as err:
        return pack_err(str(err))

    return pack_success(auction_info.to_json())

# Requires: id (int), ID of existing auction
@app.route("/start_auction",methods=["PATCH"])
def start_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        accessor.update_auction(auction_id, "status", auction_status["online"])
    except Exception as err:
        return pack_err(str(err))

    return json_success()

# Requires: id (int), ID of existing auction
@app.route("/end_auction_by_time",methods=["PATCH"])
def end_auction_by_time():
    # TODO: call shopping API and place item in user's cart
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        accessor.update_auction(auction_id, "status", auction_status["ended_by_time"])
    except Exception as err:
        return pack_err(str(err))

    try:
        auction = accessor.get_auction_by_id(auction_id)
    except Exception as err:
        return pack_err(str(err))
    
    item_id = auction.item_id
    winning_bid_id = auction.current_highest_bid_id

    if winning_bid_id is None:
        # Notify seller that nobody bid
        return json_success()

    try:
        winning_bid = accessor.get_bid_by_id(winning_bid_id)
    except Exception as err:
        return pack_err(str(err))

    try:
        winning_bid_amount = winning_bid.bid_amount
        accessor.update_auction(auction_id, "finished_price", winning_bid_amount)
    except Exception as err:
        return pack_err(str(err))

    try:
        winner = winning_bid.user_id
        accessor.update_auction(auction_id, "finished_user", winner)
    except Exception as err:
        return pack_err(str(err))

    try:
        post_data = {"id": item_id, "price": winning_bid_amount}
        update_item = requests.post(inventory_url + "update_item", json=post_data)
    except Exception as err:
        return pack_err(str(err))

    check_update_item = check_success(update_item)
    if not check_update_item:
        return pack_err("Unable to update item price.")

    try:
        put_data = "add_item_to_cart?id={}&item={}&quantity=1".format(winner, item_id)
        add_to_cart = requests.put(shopping_url + put_data)
    except Exception as err:
        return pack_err(str(err))

    check_add_to_cart = check_success(add_to_cart)
    if not check_add_to_cart:
        return pack_err("Unable to add item to cart.")

    return json_success()

# Requires: id (int), ID of existing auction
@app.route("/end_auction_by_purchase",methods=["PATCH"])
def end_auction_by_purchase():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        accessor.update_auction(auction_id, "status", auction_status["purchased_by_buy_now"])
    except Exception as err:
        return pack_err(str(err))

    return json_success()

# Requires: id (int), ID of existing auction
@app.route("/cancel_auction",methods=["PATCH"])
def cancel_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        accessor.update_auction(auction_id, "status", auction_status["canceled"])
    except Exception as err:
        return pack_err(str(err))

    return json_success()

# Requires: id (int), ID of existing bid
@app.route("/get_bid",methods=["GET"])
def get_bid():
    accessor = AuctionAccessor()
    bid_id = request.args.get("id")

    try:
        bid_info = accessor.get_bid_by_id(bid_id)
    except Exception as err:
        return pack_err(str(err))

    return pack_success(bid_info.to_json())

# Requires: id (int), ID of existing auction
@app.route("/get_bids_by_auction",methods=["GET"])
def get_bids_by_auction():
    accessor = AuctionAccessor()
    auction_id = request.args.get("id")

    try:
        bids = accessor.get_bids_by_auction(auction_id)
    except Exception as err:
        return pack_err(str(err))

    json_bids = []
    for bid in bids:
        json_bids.append(bid.to_json())

    return pack_success(json_bids)

# -------- inner functions ----------
def check_auction_input(data):
    try:
        start_time = data.get("start_time")
        assert start_time is not None, "invalid start time"
        assert isinstance(start_time, str), "invalid start time"
        end_time = data.get("end_time")
        assert end_time is not None, "invalid end time"
        assert isinstance(end_time, str), "invalid end time"
        start_price = data.get("start_price")
        assert start_price is not None, "invalid start price"
        assert isinstance(start_price, float) or isinstance(start_price, int), "invalid start price"
        item_id = data.get("item_id")
        assert item_id is not None, "invalid item id"
        assert isinstance(item_id, int), "invalid item id"
    except Exception as e:
        print("create_auction param error %s"%e)
        return False, "Invalid or missing parameter"
    return True, ""

def check_bid_input(data):
    try:
        auction_id = data.get("auction_id")
        assert auction_id is not None, "invalid auction id"
        assert isinstance(auction_id, int), "invalid auction id"
        user_id = data.get("user_id")
        assert user_id is not None, "invalid user id"
        assert isinstance(user_id, str), "invalid user id"
        bid_amount = data.get("bid_amount")
        assert bid_amount is not None, "invalid bid amount"
        assert isinstance(bid_amount, float) or isinstance(bid_amount, int), "invalid bid amount"
    except Exception as e:
        print("place_bid param error %s"%e)
        return False, "Invalid or missing parameter"
    return True, ""

def check_success(response):
    response = json.loads(response.text)
    return response.get("status")

def try_notify_bidder(accessor: AuctionAccessor, winning_bid_id: int):
    try:
        winning_bid = accessor.get_bid_by_id(winning_bid_id)
    except Exception as err:
        return str(err)
    losing_user = winning_bid.user_id

    subject = "You've been outbid."
    body = "Someone else just bid higher than you on an auction."

    try:
        response = requests.get(account_url + str(losing_user))
    except Exception as err:
        return str(err)

    try:
        response = json.loads(response.text)
    except json.decoder.JSONDecodeError as err:
        return str(err)

    losing_user_email = response.get("email")
    post_data = {"subject": subject, "body": body, "to": losing_user_email}
    
    # We should still allow bid even if email fails
    requests.post(email_url + "send_email", json=post_data)

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
    port = int(os.environ.get("PORT", 5003))
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port=port)
