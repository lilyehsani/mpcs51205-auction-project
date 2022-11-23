from datetime import datetime


class Cart:
    def __init__(self, cart_id: int, user_id: int, create_time: datetime, checkout_time: datetime):
        self.cart_id = cart_id
        self.user_id = user_id
        self.create_time = create_time
        self.checkout_time = checkout_time

    def to_json(self):
        return {
            "cart_id": str(self.cart_id),
            "user_id": str(self.user_id),
            "create_time": str(self.create_time),
            "checkout_time": str(self.checkout_time)
        }