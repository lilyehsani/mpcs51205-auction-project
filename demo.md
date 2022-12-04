# Set up

- docker-compose up --force-recreate --build
  - Wait for the command to finish. It will take around 30 seconds. You will know it's finished when the three MySQL Flask services display as up and running.

# Create users (Account Service)

- curl --location --request GET 'http://127.0.0.1:5005/account/ping'
  - Checks on the service. Should just return "message": "Ping success".
- curl --location --request POST 'http://127.0.0.1:5005/account' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "test1",
  "status": 0,
  "email": "test1",
  "seller_rating": "4.5",
  "user_name": "ted_wang",
  "user_password": "ted_wang_password"
  }'
  - Creates an account. Should return the id of the new account. Save this for later. Id: 63852bdf87c0fbc5fa2de9f9
- curl --location --request GET 'http://127.0.0.1:5005/account/638532faac31660c30282fcd'
  - Shows that the account has been created. Will not show the password.

# Create an item (Inventory Service)

- curl --location --request POST 'http://127.0.0.1:5001/create_item' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "name": "Pants",
  "quantity": 1,
  "description": "Cozy warm pants!",
  "shipping_cost": 3,
  "is_buy_now": true,
  "price": 100,
  "category_id": 1,
  "user_id": 3
  }'
  - Creates an item being sold by user with id 1. Id: 1
- curl --location --request POST 'http://127.0.0.1:5001/create_item' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name":"aaaa",
  "quantity":6,
  "description":"desc",
  "shipping_cost": 3,
  "is_buy_now": true,
  "price":222,
  "category_id":1,
  "user_id": 1
  }'
  - Creates an item being sold by user with id 1. Id: 2
- curl --location --request POST 'http://127.0.0.1:5001/create_item' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name":"bbb",
  "quantity":8,
  "description":"desc",
  "shipping_cost": 3,
  "is_buy_now": false,
  "price":222,
  "category_id":1,
  "user_id": "6385203bc55c6662f7b05ed6"
  }'

  - Creates an item being sold by user with id 1. Id: 3

- curl --location --request GET 'http://127.0.0.1:5001/get_items?ids=1,2,3'

  - Gets information about all 3 of our items.

- curl --location --request GET 'http://127.0.0.1:5001/search_item?keyword=aa'

  - Searches for items with aa in the name.

- curl --location --request POST 'http://127.0.0.1:5001/create_category' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "Clothes"
  }'

  - Creates the clothes category. Id: 2

- curl --location --request POST 'http://127.0.0.1:5001/comsume_availble_items' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "id_list": [2, 3],
  "quantity_list": [5, 8]
  }'

  - Consumes the items (like when a user checks out).

- curl --location --request GET 'http://127.0.0.1:5001/get_items?ids=1,2,3'
  - Shows that items 2 and 3 now have quantity 1 and 0.

# Create an auction (Auction and Shopping Services)

- curl --request POST 'http://127.0.0.1:5003/create_auction' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "start_time":"2022-11-28 16:15:00",
  "end_time":"2022-11-28 16:16:00",
  "start_price": 20.00,
  "item_id": 1
  }'

  - Creates an auction for the item with id 1.

- curl --location --request PATCH 'http://127.0.0.1:5003/start_auction?id=1'

  - Manually starts the auction (the queue can do this but it might not be fun for the demo).

- curl --request POST 'http://127.0.0.1:5003/place_bid' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "auction_id":1,
  "user_id":1,
  "bid_amount":19.99
  }'

  - Shows that you can't place a bid below the starting price.

- curl --request POST 'http://127.0.0.1:5003/place_bid' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "auction_id":1,
  "user_id":1,
  "bid_amount":30.50
  }'

  - Places a bid of 30.50.

- curl --request POST 'http://127.0.0.1:5003/place_bid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "auction_id":1,
  "user_id":2,
  "bid_amount":35.50
  }'

  - Places a bid of 35.50.

- curl --request POST 'http://127.0.0.1:5003/place_bid' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "auction_id":1,
  "user_id":1,
  "bid_amount":35.00
  }'

  - Tries to place a bid of 35.00, will fail as it's not higher than the current highest bid.

- curl --location --request PATCH 'http://127.0.0.1:5003/end_auction_by_time?id=1'

  - Manually ends the auction (the queue can do this but it might not be fun for the demo).

- curl --request POST 'http://127.0.0.1:5003/place_bid' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "auction_id":1,
  "user_id":1,
  "bid_amount":36.00
  }'

  - Tries to place a bid of 36.00, will fail as the auction is over.

- curl --location --request GET 'http://127.0.0.1:5001/get_items?ids=1'

  - Shows that the price has been set by the winning of the auction as the winning bid amount.

- curl --location --request GET 'http://127.0.0.1:5002/get_items_in_cart?id=2'

  - Shows that the item is in the winning user's cart.

- curl --location --request POST 'http://127.0.0.1:5002/checkout' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "user_id":2
  }'

  - Checks out the user's cart.

- curl --location --request GET 'http://127.0.0.1:5002/get_items_in_cart?id=2'
  - Shows that the item is no longer in winning user's cart.

# Auction queue

- Uncomment auction queue service in docker-compose.yml

  - Explain that it works as a cron job that runs every 10 minutes checking if any auctions need to be started or ended. It will run for the first time on the nearest 10 minute mark.
  - Running it right now just for the demo, it will run every minute instead.

- curl --location --request POST 'http://127.0.0.1:5001/create_item' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "name": "Pants",
  "quantity": 1,
  "description": "Cozy warm pants!",
  "shipping_cost": 3,
  "is_buy_now": true,
  "price": 100,
  "category_id": 1,
  "user_id": 3
  }'

  - Creates an item being sold by user with id 1. Id: 1

- curl --request POST 'http://127.0.0.1:5003/create_auction' \
   --header 'Content-Type: application/json' \
   --data-raw '{
  "start_time":"2022-11-28 16:28:00",
  "end_time":"2022-11-28 16:29:00",
  "start_price": 20.00,
  "item_id": 1
  }'

  - Creates an auction for the item with id 1. Change the times so that it will start in a minute and end a minute after that.

- curl --location --request GET 'http://127.0.0.1:5003/get_all_auction'
  - Repeat this command while the queue is working to see how the auction's status changes.
