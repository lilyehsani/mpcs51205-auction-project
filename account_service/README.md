## Create a network
docker network create account-service-network

## Create the account-service image
docker build -t account-service:latest .

## Run containers
docker run -d --network account-service-network -p 27017:27017 --name account_service_db mongo
docker run -d --name account_service --network account-service-network -p 5000:5000 account-service

## Run Account Service
Try to call the APIs

### ping
GET http://127.0.0.1:5000/account/ping

### createAccount
POST http://127.0.0.1:5000/account
```
{
    "name": "test",
    "status": 0,
    "email": "test",
    "seller_rating": "1.1",
    "user_name": "ted_wang",
    "user_password": "ted_wang"
}
```

A account ID should be returned. Let's say it's <returned_id>

### getAccount
GET http://127.0.0.1:5000/account/<returned_id>

Should return something like this
```
{
    "email": 0,
    "id": "63803a221c6c16e4133230ab",
    "name": "test",
    "seller_rating": "1.1",
    "status": 0,
    "user_name": "ted_wang"
}
```

### updateAccount
PUT http://127.0.0.1:5000/account/<returned_id>

with body
```
{
    "name": "puttest",
    "status": 0,
    "email": "test",
    "seller_rating": "1.1",
    "user_name": "puttest",
    "user_password": "puttest"
}
```

### delete
DELETE http://127.0.0.1:5000/account/<returned_id>
