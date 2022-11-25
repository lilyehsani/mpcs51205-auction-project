## Create a network
docker network create account-service-network

## Create the account-service image
docker build -t account-service:latest .

## Run containers
docker run -d --network account-service-network -p 27017:27017 --name account_service_db mongo
docker run -d --name account_service --network account-service-network -p 5000:5000 account-service
