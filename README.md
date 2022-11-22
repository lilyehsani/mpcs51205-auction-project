# mpcs51205-auction-project

MPCS 51205 Topics in Software Engineering group project by Lily Ehsani, Yuke Gong, Yunchen Liu, and Wei Shi (Ted) Wang

# system setup

./run.sh

# test inventory

- run the whole system:
  ./run.sh

- home page for test:
  curl -X GET http://localhost:5001/

- create item:
  curl --request POST 'http://127.0.0.1:5001/create_item' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name":"bbb",
  "quantity":2,
  "description":"desc",
  "shipping_cost": 3,
  "is_buy_now": true,
  "price":222
  }'

- get an item (replace an_item_id with a real id)
  curl --location --request GET 'http://127.0.0.1:5001/get_item?id=an_item_id'

- change item quantity (replace an_item_id with a real id)
  curl --request POST 'http://127.0.0.1:5001/change_item_cnt' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "id": "an_item_id",
  "quantity":4
  }'

## Auction Service

Prerequisites: docker and docker compose.
To start up the auction database and service, run `docker compose up` from the root directory. It usually takes about 30 seconds, because the service container has to wait for the database container to be up and running before it does anything.

To use the auction service:

- Create auction (with example values):
  curl --request POST 'http://127.0.0.1:5002/create_auction' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "start_time":"2022-11-21 18:29:40",
  "end_time":"2022-11-21 20:29:40",
  "quantity":1,
  "item_id": 5
  }'

- Place bid (wih example values):
  curl --request POST 'http://127.0.0.1:5002/place_bid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "auction_id":1,
  "user_id":2,
  "bid_amount":40.50
  }'

- Get all auctions:
  curl --location --request GET 'http://127.0.0.1:5002/get_all_auction'

- Get auction by id (change <id> to the auction's id):
  curl --location --request GET 'http://127.0.0.1:5002/get_auction?id=<id>'

- Start auction (change <id> to the auction's id):
  curl --location --request POST 'http://127.0.0.1:5002/start_auction?id=<id>'

- End auction due to time (change <id> to the auction's id):
  curl --location --request POST 'http://127.0.0.1:5002/end_auction_by_time?id=<id>'

- End auction due to a "buy now" purchase of the item (change <id> to the auction's id):
  curl --location --request POST 'http://127.0.0.1:5002/end_auction_by_purchase?id=<id>'

- Cancel an auction (change <id> to the auction's id):
  curl --location --request POST 'http://127.0.0.1:5002/cancel_auction?id=<id>'

## For Users DB

- Install docker
- `docker run -d -p 27017:27017 --name user_service_db mongo`
- cd `mongo-db` and run `users_db.py`
  Should output the following row and saved in the docker mongoDB `auctiondb` and table `users`:

```
{'_id': ObjectId('6360afed0d873cec09f2eab0'), 'user_id': 1, 'name': 'Ted', 'status': 0, 'email': 'weishi830@hotmail.com', 'seller_rating': 4.1}
```

- As long as the docker container does not get killed, the data in db will be preserved.

## For Items DB

- Install docker
- `docker run -d -p 27017:27017 --name inventory_service_db mongo`
- cd `mongo-db` and run `items_db.py`
  Should output the following row and saved in the docker mongoDB `inventorydb` and table `items`:

```
{'_id': ObjectId('63647af674f3beb5c5df472c'), 'item_id': 1, 'name': 'iPhone14', 'description': 'color: black', 'quantity': 1, 'shipping_cost': 6.8, 'is_buy_now': False, 'price': 1000, 'status': 0}
```

- As long as the docker container does not get killed, the data in db will be preserved.

# MySQL in docker setup

For Shopping DB:

- `docker run --name=shopping_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3307:3306 -d mysql:latest`
- `cd mysql-db`
- `python3 shopping_db.py`
  You should see:

```
cart table:
(1, 1, datetime.datetime(2022, 11, 19, 11, 6, 13), datetime.datetime(2022, 11, 19, 13, 6, 13))
cart_item table:
(1, 1)
user_item table:
(1, 1)
```

For Inventory DB:

- `docker run --name=inventory_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3309:3306 -d mysql:latest`
- `cd mysql-db`
- `python3 inventory_db.py`
  You should see:

```
categories table:
(1, 'Food')
category_item table:
(1, 1)
item table:
(1, 'Bubble Tea', 'Watermelon jasmine flavor', 1, 3.0, 0, 6.8, 0)
```

For Auction DB:

(Do not do this anymore. Use docker compose as described above instead.)

- If you have not run the db before, do: `docker run --name=auction_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3308:3306 -d mysql:latest`
- If you have run the db before, do: `docker start auction_db`
- `cd auction_service`
- `python3 init_auction_db.py`
  You should see something like:

```
Current tables in auction_db:
('Auction',)
('AuctionItem',)
('Bid',)
Current auctions in Auction table:
(1, datetime.datetime(2022, 11, 18, 21, 6, 35), datetime.datetime(2022, 11, 18, 23, 6, 35), 1, 0, None, None, None)
(2, datetime.datetime(2022, 11, 18, 23, 6, 35), datetime.datetime(2022, 11, 19, 1, 6, 35), 4, 0, None, None, None)
Current auction-items in AuctionItem table:
(1, 5)
(2, 6)
Current bids in Bid table:
(1, 1, 1, 20.5, datetime.datetime(2022, 11, 18, 21, 8, 35))
(2, 1, 2, 25.5, datetime.datetime(2022, 11, 18, 21, 9, 35))
(3, 1, 1, 30.5, datetime.datetime(2022, 11, 18, 21, 10, 35))
```

(but it will have a different dates as they are based on the current time). This represents 2 auctions, one of which is happening now and one which takes place in two hours. The first is of the item with id=5, the second of the item with id=6. Three bids have been placed on the auction that is online.

## Send Email API

The api link is https://zvhfeuzz3m.execute-api.us-east-1.amazonaws.com/Prod/mail/

It's a POST API. The body is of the following format:

```
{
  "subject": "This is a test",
  "body": "Congrats, it works!",
  "to":"weishi830@hotmail.com"
}
```

The email will be sent from the email address of `random.name.mpcs51205@gmail.com`.

The response should be in the form of:

```
{
    "source_email": "random.name.mpcs51205@gmail.com",
    "destination_email": "weishi830@hotmail.com",
    "subject": "This is a test",
    "body": "Congrats, it works!",
    "status": "success"
}
```
