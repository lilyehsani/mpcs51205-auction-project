from datetime import datetime

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Bid:
    '''
    Stores information related to a single bid. Must have a bid ID, auction ID, user ID (bidder),
    bid amount (float or int), and bid time.
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