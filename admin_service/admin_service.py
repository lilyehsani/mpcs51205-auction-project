from flask import Flask, request, jsonify
from datetime import datetime
import os
import json

from flaskr.accessor.admin_accessor import AdminAccessor

app = Flask(__name__)

# -------- open APIs ----------
@app.route("/")
def home():
    return "admin routers page"

# Requires: sender (str), body (str)
@app.route("/create_email",methods=["POST"])
def create_email():
    data = request.get_data()
    data = json.loads(data)
    check_result, err = check_email_input(data)
    if not check_result:
        return pack_err(str(err))

    accessor = AdminAccessor()

    try:
        accessor.create_email(data.get("sender"), datetime.now(), data.get("body"))
    except Exception as err:
        return pack_err(str(err))

    return json_success()

# Requires: None
@app.route("/get_all_email",methods=["GET"])
def get_all_email():
    accessor = AdminAccessor()

    try:
        emails = accessor.get_all_email()
    except Exception as err:
        return pack_err(str(err))

    json_emails = []
    for email in emails:
        json_emails.append(email.to_json())

    return pack_success(json_emails)

# Requires: id (str)
@app.route("/get_email",methods=["GET"])
def get_email():
    accessor = AdminAccessor()
    email_id = request.args.get("id")

    try:
        email = accessor.get_email_by_id(email_id)
    except Exception as err:
        return pack_err(str(err))
    
    return pack_success(email.to_json())

# Requires: id (str)
@app.route("/register_response",methods=["PATCH"])
def register_response():
    accessor = AdminAccessor()
    email_id = request.args.get("id")

    try:
        accessor.update_email(email_id, "responded_time", format_time(datetime.now()))
    except Exception as err:
        return pack_err(str(err))

    return json_success()

# -------- inner functions ----------
def check_email_input(data):
    try:
        sender = data.get("sender")
        assert sender is not None, "invalid sender"
        assert isinstance(sender, str), "invalid start time"
        body = data.get("body")
        assert body is not None, "invalid start price"
        assert isinstance(body, str), "invalid start price"
    except Exception as e:
        print("create_email param error %s"%e)
        return False, "Invalid or missing parameter"
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

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5006))
    app.run(debug=True, host="0.0.0.0", port=port)