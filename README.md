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

- Install docker
- `docker run --name=user_mysql_1 --env="MYSQL_ROOT_PASSWORD=root_password" -p 3307:3306 -d mysql:latest`
- `cd mysql-db`
- `python3 mysql_default.py`
  The result should show tables including UserItem, Categories and CategoriesItem. Also a piece of test data should show up:

```
('Categories',)
('CategoriesItem',)
('UserItem',)
(1234, 6789)
```

For Auction DB:

- If you have not run the db before, do: `docker run --name=auction_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3308:3306 -d mysql:latest`
- If you have run the db before, do: `docker start auction_db`
- `cd mysql-db`
- `python3 auction_db.py`
  You should see:

```
Current tables in auction_db:
('Auction',)
('AuctionItem',)
('Bid',)
Current auctions in Auction table:
(1234, datetime.datetime(2022, 11, 18, 12, 31, 59), datetime.datetime(2022, 11, 18, 14, 31, 59), 1, 0, 0, 0.0, 0)
Current auction-items in AuctionItem table:
(1234, 5)
Current bids in Bid table:
(1, 1234, 6, 20.5, datetime.datetime(2022, 11, 18, 12, 33, 59))
```

(but it will have a different dates as they are based on the current time).

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
