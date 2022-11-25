from flaskr.accessor.account_accessor import AccountAccessor
from flaskr.model.user import User


class AccountService:
    _account_accessor: AccountAccessor

    def __init__(self, account_accessor: AccountAccessor):
        self._account_accessor = account_accessor

    def create_user(self, name: str, status: int, email: str, seller_rating: str, user_name: str,
                    user_password: str) -> str:
        return self._account_accessor.create_user(name, status, email, seller_rating, user_name, user_password)

    def get_user_by_id(self, user_id: str) -> User:
        return self._account_accessor.get_user_by_id(user_id)

    def update_user(self, user_id: str, name: str, status: int, email: str, seller_rating: str, user_name: str,
                    user_password: str):
        return self._account_accessor.update_user(user_id, name, status, email, seller_rating, user_name, user_password)

    def delete_user(self, user_id: str):
        return self._account_accessor.delete_user(user_id)
