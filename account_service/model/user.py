class User:
    def __init__(self, user_id: int, name: str, status: int,
                 email: str, seller_rating: str, user_name: str):
        self.user_id = user_id
        self.name = name
        self.status = status
        self.email = email
        self.seller_rating = seller_rating
        self.user_name = user_name
