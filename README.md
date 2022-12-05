# mpcs51205-auction-project

MPCS 51205 Topics in Software Engineering group project by Lily Ehsani, Yuke Gong, Yunchen Liu, and Wei Shi (Ted) Wang

# For Professor and TA's

Note: The service will automatically create some support emails on startup. The support emails will have the sender field set to lilytehsani@gmail.com. If you want them to be from your email (to test the responding to email functionality), please change this field located at 'mpcs51205-auction-project/auction_queue/admin_email_data.py' in the `senders` list.

To start our project, you must have docker and docker-compose installed. To run the backend, run:
`docker-compose up --force-recreate --build`
This will take 30-45 seconds to get everything up and running, because the backend services have to wait for the DB services to be healthy. You will know it is done when the output of that command shows these three services: mpcs51205-auction-project-shopping_service-1, mpcs51205-auction-project-auction_service-1, and mpcs51205-auction-project-inventory_service-1 with the output " \* Debugger is active!".
To run the webapp frontend, once the backend is up, `cd` into the directory `ui/src`, then run `npm start`. It should open localhost:3000/dashboard.

From there, you can use the webapp to explore the system. If you open the console, you will likely see logging output and (hopefully not) error output, should any arise.

The rest of this document gives more details about each API.

# system setup

./run.sh

# test inventory

- run the inventory microservice with db:
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
  "price":222,
  "category_id":1
  }'

- get an item (replace an_item_id with a real id)
  curl --location --request GET 'http://127.0.0.1:5001/get_items?id=an_item_id'

## Auction Service

Prerequisites: docker and docker compose.
To start up the auction database and service, run `docker compose up` or `docker-compose up --force-recreate --build` from the root directory. It usually takes about 30 seconds, because the service container has to wait for the database container to be up and running before it does anything.

To use the auction service:

- Create auction (with example values):
  curl --request POST 'http://127.0.0.1:5003/create_auction' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "start_time": "2022-11-21 18:29:40",
  "end_time": "2022-11-21 20:29:40",
  "item_id": 5
  }'

- Place bid (wih example values):
  curl --request POST 'http://127.0.0.1:5003/place_bid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "auction_id": 1,
  "user_id": "123454135",
  "bid_amount":40.50
  }'

- Get all auctions:
  curl --location --request GET 'http://127.0.0.1:5003/get_all_auction'

- Get all startable auctions (where status = 0):
  curl --location --request GET 'http://127.0.0.1:5003/get_all_startable_auction'

- Get all endable auctions (where status = 1):
  curl --location --request GET 'http://127.0.0.1:5003/get_all_endable_auction'

- Get auctions by item id (change <id> to the auction's id):
  curl --location --request GET 'http://127.0.0.1:5003/get_auctions_by_item_id?id=<id>'

- Get auction by auction id (change <id> to the auction's id):
  curl --location --request GET 'http://127.0.0.1:5003/get_auction?id=<id>'

- Start auction (change <id> to the auction's id):
  curl --location --request PATCH 'http://127.0.0.1:5003/start_auction?id=<id>'

- End auction due to time (change <id> to the auction's id):
  curl --location --request PATCH 'http://127.0.0.1:5003/end_auction_by_time?id=<id>'

- End auction due to a "buy now" purchase of the item (change <id> to the auction's id):
  curl --location --request PATCH 'http://127.0.0.1:5003/end_auction_by_purchase?id=<id>'

- Cancel an auction (change <id> to the auction's id):
  curl --location --request PATCH 'http://127.0.0.1:5003/cancel_auction?id=<id>'

## Admin service

- Create complaint email
  curl --location --request POST 'http://127.0.0.1:5006/create_email' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "sender": "sender@gmail.com",
  "body": "Bad website!"
  }'

- Get all complaint emails
  curl --location --request GET 'http://127.0.0.1:5006/get_all_email'

- Get complaint email by ID
  curl --location --request GET 'http://127.0.0.1:5006/get_email?id=<id>'

## Shopping Service

To start up the shopping service and database, please run 'run.sh' and 'flaskr/routers.py'

To use the shopping service:

- Create an item for sale: curl --location --request POST 'http://127.0.0.1:5000/create_item'
- Get items for sale by owner: curl --location --request GET 'http://127.0.0.1:5000/get_items_for_sale?user_id=<user_id>'
- Remove item for sale: curl --location --request POST 'http://127.0.0.1:5000/remove_item_for_sale'
- Add an item to cart: curl --location --request PUT 'http://127.0.0.1:5000/add_item_to_cart?id=<user_id>&item=<item_id>&quantity=<quantity>'
- Get items in cart by user: curl --location --request GET 'http://127.0.0.1:5000/get_items_in_cart?id=<user_id>'
- Remove an item from cart: curl --location --request DELETE 'http://127.0.0.1:5000/remove_item_from_cart?id=<user_id>&item=<item_id>'
- Checkout items in cart: curl --location --request POST 'http://127.0.0.1:5000/checkout?user_id=<user_id>'

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
