import pymongo  # package for working with MongoDB
from bson import ObjectId

from model.user import User

db_address: str = "mongodb://localhost:27017/"
db_name: str = "accountdb"
table_name: str = "users"


class AccountAccessor:
    def __init__(self):
        self.client = pymongo.MongoClient(db_address)
        self.db = self.client[db_name]
        self.table = self.db[table_name]

    def create_user(self, name: str, status: int, email: str, seller_rating: str, user_name: str,
                    user_password: str) -> str:
        # Check duplicates
        existing_users = list(self.table.find(
            {"user_name": user_name}
        ))
        if existing_users:
            raise Exception("The user name already exist. Please try a different one.")

        user = {"name": name, "status": status, "email": email, "seller_rating": seller_rating, "user_name": user_name,
             "user_password": user_password}

        return self.table.insert_one(user).inserted_id

    def get_user_by_id(self, user_id) -> User:
        existing_user = self.table.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise Exception("This user does not exist.")

        return User(existing_user.get('_id'),
                    existing_user.get('name'),
                    existing_user.get('status'),
                    existing_user.get('email'),
                    existing_user.get('seller_rating'),
                    existing_user.get('user_name')
                    )

    def get_user(self, user_name, user_password) -> User:
        existing_users = list(self.table.find(
            {"user_name": user_name, "user_password": user_password}
        ))

        if not existing_users:
            raise Exception("The user name or password is not correct")

        existing_user = existing_users[0]

        return User(existing_user.get('_id'),
                    existing_user.get('name'),
                    existing_user.get('status'),
                    existing_user.get('email'),
                    existing_user.get('seller_rating'),
                    existing_user.get('user_name')
                    )

    def update_user(self, user_id: str, name: str, status: int, email: str, seller_rating: str, user_name: str,
                    user_password: str) -> None:
        query = {"_id": ObjectId(user_id)}
        existing_user = self.table.find_one(query)

        if not existing_user:
            raise Exception("This user does not exist.")

        self.table.update_one(query, {"name": name, "status": status, "email": email, "seller_rating": seller_rating,
                                      "user_name": user_name,
                                      "user_password": user_password})

    def delete_user(self, user_id: str) -> None:
        query = {"_id": ObjectId(user_id)}
        existing_user = self.table.find_one(query)

        if not existing_user:
            raise Exception("This user does not exist.")

        self._soft_delete(query, existing_user)

    def _soft_delete(self, query: dict, existing_user: dict):
        self.table.update_one(query, {"name": existing_user.get('name'),
                                      "status": -1,
                                      "email": existing_user.get('email'),
                                      "seller_rating": existing_user.get('seller_rating'),
                                      "user_name": existing_user.get('user_name'),
                                      "user_password": existing_user.get('user_password')
                                      })

    def hard_delete_user(self, user_id: str) -> int:
        return self.table.delete_one({'_id': ObjectId(user_id)}).deleted_count

    def suspend_user(self, user_id: str) -> None:
        query = {"_id": ObjectId(user_id)}
        existing_user = self.table.find_one(query)

        if not existing_user:
            raise Exception("This user does not exist.")

        self._suspend(query, existing_user)

    def _suspend(self, query, existing_user):
        self.table.update_one(query, {"name": existing_user.get('name'),
                                      "status": 0,
                                      "email": existing_user.get('email'),
                                      "seller_rating": existing_user.get('seller_rating'),
                                      "user_name": existing_user.get('user_name'),
                                      "user_password": existing_user.get('user_password')
                                      })
