from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests
import json
import random

from admin_email_data import senders, bodies

api_url_if_docker = "http://auction_service:5003/"
api_url_if_local = "http://127.0.0.1:5003/"
auction_url = api_url_if_docker
admin_url = "http://admin_service:5006/"

#-------- inner functions ----------
# Gets the soonest exact 10 minute time (i.e., time ends in 00, 10, 20, 30...)
# Adds a 5 second buffer just in case
def get_nearest_10_min():
    now = datetime.now()

    now_minute = now.minute
    if now_minute < 10:
        now_minute_str = "0" + str(now_minute)
    else:
        now_minute_str = str(now_minute)

    first_digit = now_minute_str[0]
    new_minute = int(first_digit + "0")

    start = datetime(now.year, now.month, now.day, now.hour, new_minute, 5) + timedelta(minutes=10)

    return start

# "Sends" a complaint email to the database twice a day, at 10:00am and 6:00pm
def send_complaint_email():
    sender_index = random.randint(0, (len(senders) - 1))
    body_index = random.randint(0, (len(bodies) - 1))
    post_data = {"sender": senders[sender_index], "body": bodies[body_index]}
    try:
        response = requests.post(admin_url + "create_email", json=post_data)
    except Exception:
        print("Complaint email couldn't be sent.")

    response = json.loads(response.text)
    if not response.get("status"):
        print("Complaint email couldn't be sent.")
        

def start_auctions():
    startable = requests.get(auction_url + "get_all_startable_auction")
    data = json.loads(startable.text)
    if not data.get("status"):
        raise Exception("JSON Error")
    for auction in data.get("data"):
        auction_id = auction["id"]
        start_time_str = auction["start_time"]
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        if start_time <= datetime.now():
            patch = auction_url + "start_auction?id={}".format(auction_id)
            response = requests.patch(patch)
            response_json = json.loads(response.text)
            if not response_json.get("status"):
                err_msg = "Unable to start auction with id={} that should be started at {}".format(
                    auction_id, start_time_str)
                raise Exception(err_msg)

def end_auctions():
    endable = requests.get(auction_url + "get_all_endable_auction")
    data = json.loads(endable.text)
    if not data.get("status"):
        raise Exception("JSON Error")
    for auction in data.get("data"):
        auction_id = auction["id"]
        end_time_str = auction["end_time"]
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        if end_time <= datetime.now():
            patch = auction_url + "end_auction_by_time?id={}".format(auction_id)
            response = requests.patch(patch)
            response_json = json.loads(response.text)
            if not response_json.get("status"):
                err_msg = "Unable to end auction with id={} that should be ended at {}".format(
                    auction_id, end_time_str)
                raise Exception(err_msg)

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

#-------- job queue ----------
def start_and_end_auctions():
    now = datetime.now()

    # Starts and ends startable/endable auctions
    start_auctions()
    end_auctions()

    # "Sends" complaint emails to the database twice a day, at 10:00am and 6:00pm
    now_minute = now.minute
    now_hour = now.hour
    if now_minute < 10 and (now_hour == 10 or now_hour == 18):
        send_complaint_email()

result = None
while result is None:
    try:
        result = requests.get(auction_url + "get_all_auction")
    except requests.exceptions.ConnectionError as err:
        time.sleep(2)

# Start off with 2 complaint emails
send_complaint_email()
send_complaint_email()

sched = BackgroundScheduler(daemon=True)

# sched.add_job(start_and_end_auctions,'interval',minutes=1)
sched.add_job(start_and_end_auctions,'interval',minutes=10,start_date=get_nearest_10_min())
sched.start()

while True:
    time.sleep(10)
sched.shutdown()
