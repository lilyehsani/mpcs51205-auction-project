from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests
import json

api_url_if_docker = "http://auction_service:5003/"
api_url_if_local = "http://127.0.0.1:5003/"
api_url = api_url_if_docker
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

def start_auctions():
    # r = requests.get("http://auction_service:5003/get_all_startable_auctions")
    startable = requests.get(api_url + "get_all_startable_auction")
    data = json.loads(startable.text)
    if not data.get("status"):
        # error
        raise Exception("JSON Error")
    for auction in data.get("data"):
        auction_id = auction["id"]
        start_time_str = auction["start_time"]
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        # print(auction["id"])
        if start_time <= datetime.now():
            patch = api_url + "start_auction?id={}".format(auction_id)
            response = requests.patch(patch)
            response_json = json.loads(response.text)
            if not response_json.get("status"):
                err_msg = "Unable to start auction with id={} that should be started at {}".format(
                    auction_id, start_time_str)
                raise Exception(err_msg)

def end_auctions():
    endable = requests.get(api_url + "get_all_endable_auction")
    data = json.loads(endable.text)
    if not data.get("status"):
        raise Exception("JSON Error")
    for auction in data.get("data"):
        auction_id = auction["id"]
        end_time_str = auction["end_time"]
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        if end_time <= datetime.now():
            patch = api_url + "end_auction_by_time?id={}".format(auction_id)
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
    print("Running: {}".format(datetime.now()))
    print("*********** BEFORE ***********")
    res1 = requests.get(api_url + "get_all_startable_auction")
    res2 = requests.get(api_url + "get_all_endable_auction")
    print(res1.text)
    print(res2.text)
    start_auctions()
    end_auctions()
    print("*********** AFTER ***********")
    res1 = requests.get(api_url + "get_all_startable_auction")
    res2 = requests.get(api_url + "get_all_endable_auction")
    print(res1.text)
    print(res2.text)

result = None
while result is None:
    try:
        result = requests.get(api_url + "get_all_auction")
    except requests.exceptions.ConnectionError as err:
        time.sleep(2)

start = datetime.now() + timedelta(seconds=45)
a1 = {
  "start_time":format_time(start),
  "end_time":format_time(start + timedelta(minutes=1)),
  "item_id": 5
  }
a2 = {
  "start_time":format_time(start + timedelta(minutes=1)),
  "end_time":format_time(start + timedelta(minutes=2)),
  "item_id": 6
  }

res = requests.post(api_url + "create_auction", json=a1)
res1 = requests.post(api_url + "create_auction", json=a2)
print(res.text, res1.text)

sched = BackgroundScheduler(daemon=True)

print("Starting: {}".format(start))
sched.add_job(start_and_end_auctions,'interval',minutes=1,start_date=start)
# sched.add_job(start_and_end_auctions,'interval',minutes=10,start_date=get_nearest_10_min())
sched.start()

while True:
    time.sleep(10)
sched.shutdown()