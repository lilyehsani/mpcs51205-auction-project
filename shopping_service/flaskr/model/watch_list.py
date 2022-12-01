class WatchList:
    def __init__(self, id: int, user_id: int, category_id: int, max_price: float):
        self.id = id
        self.category_id = category_id
        self.user_id = user_id
        self.max_price = max_price

    def to_json(self):
        return {
            "id": str(self.id),
            "category_id": str(self.category_id),
            "user_id": str(self.user_id),
            "max_price": str(self.max_price)
        }