from datetime import datetime

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Bid:
    '''
    Stores information related to a single auction. Must have an ID, start and end times, a 
    quantity, and a status. The current highest bid is the bid ID of the bid that is currently
    winning the auction when the instance of the class is created. The finished price and
    finished user will only be set after the auction is over.
    '''
    def __init__(self, bid_id: int, auction_id: int, user_id: int, bid_amount, bid_time: datetime):
        self.bid_id = bid_id
        self.auction_id = auction_id
        self.user_id = user_id
        self.bid_amount = float(bid_amount)
        self.bid_time = bid_time

    def __repr__(self):
        res = "*** Printing Bid Information ***\n"
        res += "Bid ID: {}\nAuction ID: {}\nUser ID: {}\nBid amount: {}\nBid time: {}\n"
        res += "*** End of Bid Information ***"  
        return res.format(self.bid_id, self.auction_id, self.user_id, self.bid_amount, 
                          self.bid_time)

    def to_json(self):
        return {
            "id": self.bid_id,
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "bid_amount": self.bid_amount,
            "bid_time": format_time(self.bid_time)
        }