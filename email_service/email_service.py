from flask import Flask, request, jsonify
import os
import json
import requests

app = Flask(__name__)

# -------- open APIs ----------
@app.route("/")
def home():
    return "email routers page"

# Requires: subject (str), body (str), to (str)
@app.route("/send_email",methods=["POST"])
def send_email():
    # Get and check the input from the request
    data = request.get_data()
    data = json.loads(data)
    check_result, err = check_email_input(data)
    if not check_result:
        return pack_err(str(err))

    subject = data.get("subject")
    body = data.get("body")
    user_email = data.get("to")
    post_data = {"subject": subject, "body": body, "to": user_email}

    try:
        response = requests.post("https://zvhfeuzz3m.execute-api.us-east-1.amazonaws.com/Prod/mail/", json=post_data)
    except Exception as err:
        return pack_err(str(err))

    return pack_success(response.json())

# Requires: list of dicts with {subject (str), body (str), to (str)}
# For example:
# post_data = [{"subject": "test1", "body": "test1", "to": "lilytehsani@gmail.com"}, 
#              {"subject": "test2", "body": "test2", "to": "lilytehsani@gmail.com"}]
@app.route("/send_emails",methods=["POST"])
def send_emails():
    # Get and check the input from the request
    data = request.get_data()
    data = json.loads(data)

    # Collect errors but don't block sending of other emails
    errs = []
    for email in data:
        check_result, err = check_email_input(email)
        if not check_result:
            errs.append(str(err))
            continue
        else:
            subject = email.get("subject")
            body = email.get("body")
            user_email = email.get("to")
            post_data = {"subject": subject, "body": body, "to": user_email}

            try:
                response = requests.post("https://zvhfeuzz3m.execute-api.us-east-1.amazonaws.com/Prod/mail/", json=post_data)
            except Exception as err:
                errs.append(str(err))

            if response.status_code != 200:
                errs.append(response.text)

    if len(errs) > 0:
        return pack_err(" ".join(errs))
    else:
        return json_success()

# -------- inner functions ----------
def check_email_input(data):
    try:
        subject = data.get("subject")
        assert subject is not None, "invalid subject"
        assert isinstance(subject, str), "invalid subject"
        body = data.get("body")
        assert body is not None, "invalid body"
        assert isinstance(body, str), "invalid body"
        to = data.get("to")
        assert to is not None, "invalid to email"
        assert isinstance(to, str), "invalid to email"
    except Exception as e:
        print("send_email param error %s"%e)
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(debug=True, host="0.0.0.0", port=port)