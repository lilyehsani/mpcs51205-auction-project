from datetime import datetime

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

auction_status = {
    "created": 0,
    "online": 1,
    "ended_by_time": 2,
    "purchased_by_buy_now": 3,
    "canceled": 4
}
class Auction:
    '''
    Stores information related to a single auction. Must have an ID, start and end times, and 
    a status. The current highest bid ID is the bid ID of the bid that is currently winning the
    auction when the instance of the class is created. The finished price and finished user will
    only be set after the auction is over.
    '''
    def __init__(self, auction_id: int, item_id: int, start_time: datetime, end_time: datetime, 
                 start_price: float, status: int, current_highest_bid_id: int=None, 
                 finished_price: float=None, finished_user: int=None):
        self.auction_id = auction_id
        self.item_id = item_id
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.status = status
        self.current_highest_bid_id = current_highest_bid_id
        self.finished_price = finished_price
        self.finished_user = finished_user

    def __repr__(self):
        res = "*** Printing Auction Information ***\n"
        res += "Auction ID: {}\nStart time: {}\nEnd time: {}\nStart price: {}\n"
        res += "Status: {}\nCurrent highest bid ID: "
        res += "{}\nFinished price: {}\nFinished user ID: {}\n" 
        res += "*** End of Auction Information ***"    
        return res.format(self.auction_id, self.start_time, self.end_time, self.start_price, 
                          self.status, self.current_highest_bid_id, self.finished_price, 
                          self.finished_user)

    def to_json(self):
        return {
            "id": self.auction_id,
            "start_time": format_time(self.start_time),
            "end_time": format_time(self.end_time),
            "start_price": self.start_price,
            "status": self.status,
            "current_highest_bid_id": self.current_highest_bid_id,
            "finished_price": self.finished_price,
            "finished_user": self.finished_user
        }