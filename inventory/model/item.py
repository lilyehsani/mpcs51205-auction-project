item_status = {
    "normal": 0,
    "red_flag": 1,
    "deleted": 2,
}

class Item:
    def __init__(self,id:int, name:str, description:str, quantity:int, shipping_cost:float, is_buy_now:bool, price:float, status:int, category_id:int, category:str)-> None:
        self.id = id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.shipping_cost = shipping_cost
        self.is_buy_now = is_buy_now
        self.price = price
        self.status = status
        self.category_id = category_id
        self.category = category

    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'description':self.description,
            'quantity':self.quantity,
            'shipping_cost':self.shipping_cost,
            'is_buy_now':self.is_buy_now,
            'price':self.price,
            'status':self.status,
            'category_id':self.category_id,
            'category':self.category,
        }
        
