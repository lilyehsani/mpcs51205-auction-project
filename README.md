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

- `docker run --name=auction_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3308:3306 -d mysql:latest`
- `cd mysql-db`
- `python3 auction_db.py`
  You should see:

```
('Auction',)
(1234, datetime.datetime(2022, 11, 16, 15, 31, 19), datetime.datetime(2022, 11, 16, 17, 31, 19), 1, 0, 0, 0.0, 0)
```

(but it will have a different date as the time is current time).

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
