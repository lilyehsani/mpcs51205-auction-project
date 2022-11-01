import pymongo  # package for working with MongoDB


def insert_mock_row():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["auctiondb"]
    users = db["users"]
    user_list = [
        {"user_id": 1, "name": "Ted", "status": 0, "email": "weishi830@hotmail.com", "seller_rating": 4.1}
    ]
    users.insert_many(user_list)


def get_from_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["auctiondb"]
    users = db["users"]

    for x in users.find():
        print(x)


if __name__ == '__main__':
    insert_mock_row()
    get_from_db()

