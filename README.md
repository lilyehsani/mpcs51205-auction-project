# mpcs51205-auction-project
MPCS 51205 Topics in Software Engineering group project by Lily Ehsani, Yuke Gong, Yunchen Liu, and Wei Shi (Ted) Wang

# MongoDB in docker setup
* Install docker
* `docker run -d -p 27017:27017 --name user_service_db mongo`
* cd `mongo-db` and run `users_db.py`
Should output the following row and saved in the docker mongoDB `auctiondb` and table `users`:

```
{'_id': ObjectId('6360afed0d873cec09f2eab0'), 'user_id': 1, 'name': 'Ted', 'status': 0, 'email': 'weishi830@hotmail.com', 'seller_rating': 4.1}
```
* As long as the docker container does not get killed, the data in db will be preserved.