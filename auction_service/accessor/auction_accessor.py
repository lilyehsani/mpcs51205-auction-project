import mysql.connector
from datetime import datetime

# This is not working for some reason
# from model.auction import Auction

db_host = "localhost"
db_port = 3308
db_user = "root"
db_pwd = "root_password"
db_name = "auction_db"

class AuctionAccessor:
    '''
    Provides an interface for the Auction database. Assumes the database has been created, and its
    tables (Auction, AuctionItem, and Bid) have been set up.
    '''
    def __init__(self):
        db = mysql.connector.connect(
            host= db_host,
            port = db_port,
            user= db_user,
            password= db_pwd,
            database = db_name
        )
        self.db_connection = db
        self.cursor = db.cursor()

    def format_time(time: datetime):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    
    def create_auction(self, start_time: datetime, end_time: datetime, quantity: int, item_id: int):
        insert_auction = ("INSERT INTO Auction (start_time, end_time, quantity, status, " + 
                      "current_highest_bid, finished_price, finished_user) VALUES ('" + 
                      self.format_time(start_time) + "', '" + self.format_time(end_time) +
                      "', " + str(quantity) + ", 0, null, null, null)")
        try:
            self.cursor.execute(insert_auction)
        except mysql.connector.Error as err:
            raise Exception(err)
        auction_id = self.cursor.lastrowid
        insert_auction_item = ("INSERT INTO AuctionItem values (" + str(auction_id) + 
                            ", " + str(item_id) + ")")
        try:
            self.cursor.execute(insert_auction_item)
        except mysql.connector.Error as err:
            raise Exception(err)
        return auction_id

    def place_bid(self, auction_id: int, user_id: int, bid_amount: float, bid_time: datetime):
        insert_bid = ("INSERT INTO Bid (auction_id, user_id, bid_amount, bid_time) VALUES (" + 
                  str(auction_id) + ", " + str(user_id) + ", " + str(bid_amount) + ", '" + 
                  self.format_time(bid_time) + "')")
        try:
            self.cursor.execute(insert_bid)
        except mysql.connector.Error as err:
            raise Exception(err)
        return self.cursor.lastrowid

    def get_auction_by_id(self, auction_id: int):
        select_statement = "SELECT * FROM {} WHERE auction_id = '" + str(auction_id) + "'"
        get_auction = select_statement.format("Auction")
        self.cursor.execute(get_auction)
        auction_info = self.cursor.fetchone()
        get_item = select_statement.format("AuctionItem")
        self.cursor.execute(get_item)
        item_id = self.cursor.fetchone()[1]
        # auction = Auction(auction_info[0], item_id, auction_info[1],
        #                   auction_info[2], auction_info[3],
        #                   auction_info[4], auction_info[5],
        #                   auction_info[6], auction_info[7])
        print(self.cursor.fetchall())

    
