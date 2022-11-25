## Create a network
docker network create account-service-network

## Create the account-service image
docker build -t account-service:latest .

## Run containers
docker run -d --network account-service-network -p 27017:27017 --name account_service_db mongo
docker run -d --name account_service --network account-service-network -p 5000:5000 account-service

## Run Account Service
try to call the APIs

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