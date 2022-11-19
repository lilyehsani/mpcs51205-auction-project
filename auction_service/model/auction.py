from datetime import datetime

class Auction:
    '''
    Stores information related to a single auction. Must have an ID, start and end times, a 
    quantity, and a status. The current highest bid is the bid ID of the bid that is currently
    winning the auction when the instance of the class is created. The finished price and
    finished user will only be set after the auction is over.
    '''
    def __init__(self, auction_id: int, start_time: datetime, end_time: datetime, quantity: int,
                 status: int, current_highest_bid: int=None, finished_price: float=None, 
                 finished_user: int=None):
        self.auction_id = auction_id
        self.start_time = start_time
        self.end_time = end_time
        self.quantity = quantity
        self.status = status
        self.current_highest_bid = current_highest_bid
        self.finished_price = finished_price
        self.finished_user = finished_user

    def __repr__(self):
        res = "*** Printing Auction Information ***\n"
        res += "Auction ID: {}\nStart time: {}\nEnd time: {}\nQuantity: {}\nStatus: {}\n"
        res += "Current highest bid ID: {}\nFinished price: {}\nFinished user ID: {}\n" 
        res += "*** End of Auction Information ***"    
        return res.format(self.auction_id, self.start_time, self.end_time, self.quantity, 
                          self.status, self.current_highest_bid, self.finished_price,
                          self.finished_user)