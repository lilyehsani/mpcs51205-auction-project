from datetime import datetime

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Auction:
    '''
    Stores information related to a single auction. Must have an ID, start and end times, a 
    quantity, and a status. The current highest bid is the bid ID of the bid that is currently
    winning the auction when the instance of the class is created. The finished price and
    finished user will only be set after the auction is over.
    '''
    def __init__(self, auction_id: int, item_id: int, start_time: datetime, end_time: datetime, 
                 quantity: int, status: int, current_highest_bid_id: int=None, 
                 finished_price: float=None, finished_user: int=None):
        self.auction_id = auction_id
        self.item_id = item_id
        self.start_time = start_time
        self.end_time = end_time
        self.quantity = quantity
        self.status = status
        self.current_highest_bid_id = current_highest_bid_id
        self.finished_price = finished_price
        self.finished_user = finished_user

    def __repr__(self):
        res = "*** Printing Auction Information ***\n"
        res += "Auction ID: {}\nStart time: {}\nEnd time: {}\nQuantity: {}\nStatus: {}\n"
        res += "Current highest bid ID: {}\nFinished price: {}\nFinished user ID: {}\n" 
        res += "*** End of Auction Information ***"    
        return res.format(self.auction_id, self.start_time, self.end_time, self.quantity, 
                          self.status, self.current_highest_bid_id, self.finished_price,
                          self.finished_user)

    def to_json(self):
        return {
            "id": self.auction_id,
            "start_time": format_time(self.start_time),
            "end_time": format_time(self.end_time),
            "quantity": self.quantity,
            "status": self.status,
            "current_highest_bid_id": self.current_highest_bid_id,
            "finished_price": self.finished_price,
            "finished_user": self.finished_user
        }