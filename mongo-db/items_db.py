import pymongo  # package for working with MongoDB


def insert_mock_row():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["inventorydb"]
    items = db["items"]
    item_list = [
        {"item_id": 1, "name": "iPhone14", "description": "color: black", "quantity": 1, "shipping_cost": 6.8, "is_buy_now": False, "price": 1000, "status": 0}
    ]
    items.insert_many(item_list)


def get_from_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["inventorydb"]
    items = db["items"]

    for x in items.find():
        print(x)


if __name__ == '__main__':
    insert_mock_row()
    get_from_db()