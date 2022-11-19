import mysql.connector
from datetime import datetime, timedelta

# This is a good place to play around with Auction DB functions
# but the final accessor code will be in auction_service/auction_accessor.py
class Auction:
    '''
    Stores information related to a single auction. Must have an ID, start and end times, a 
    quantity, and a status. The current highest bid is the bid ID of the bid that is currently
    winning the auction when the instance of the class is created. The finished price and
    finished user will only be set after the auction is over.
    '''
    def __init__(self, auction_id: int, item_id: int, start_time: datetime, end_time: datetime, 
                 quantity: int, status: int, current_highest_bid: int=None, 
                 finished_price: float=None, finished_user: int=None):
        self.auction_id = auction_id
        self.item_id = item_id
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

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3308,
    'user': 'root',
    'password': 'root_password',
}

def print_from_db(cursor, message: str, table_name: str):
    print(message)
    try:
        cursor.execute("SELECT * FROM " + table_name)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return
    results = cursor.fetchall()
    for result in results:
        print(result)

def format_time(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S')

def init_db():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host= db_host,
        port = db_port,
        user= db_user,
        password= db_pwd
    )
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS auction_db")
    cursor.execute("CREATE DATABASE auction_db")
    cursor.close()

def create_auction_tables(cursor):
    # Create 3 auction-related tables
    create_auction = ("CREATE TABLE Auction (auction_id INT AUTO_INCREMENT PRIMARY KEY, " + 
                      "start_time datetime, end_time datetime, quantity int, status int, " +
                      "current_highest_bid int, finished_price float, finished_user int)")
    create_auction_item = "CREATE TABLE AuctionItem (auction_id int, item_id int)"
    create_bids = ("CREATE TABLE Bid (bid_id INT AUTO_INCREMENT PRIMARY KEY, auction_id int, " +
                   "user_id int, bid_amount float, bid_time datetime)")
    cursor.execute("DROP TABLE IF EXISTS Auction")
    cursor.execute("DROP TABLE IF EXISTS AuctionItem")
    cursor.execute("DROP TABLE IF EXISTS Bid")
    cursor.execute(create_auction)
    cursor.execute(create_auction_item)
    cursor.execute(create_bids)

    # Test creating tables
    cursor.execute("SHOW TABLES")
    print("Current tables in auction_db:")
    for x in cursor:
        print(x)

def create_new_auction(cursor, start_time: datetime, end_time: datetime, quantity: int, item_id: int):
    insert_auction = ("INSERT INTO Auction (start_time, end_time, quantity, status, " + 
                      "current_highest_bid, finished_price, finished_user) VALUES ('" + 
                      format_time(start_time) + "', '" + format_time(end_time) +
                      "', " + str(quantity) + ", 0, null, null, null)")
    try:
        cursor.execute(insert_auction)
    except mysql.connector.Error as err:
        raise Exception(err)
    auction_id = cursor.lastrowid
    insert_auction_item = ("INSERT INTO AuctionItem values (" + str(auction_id) + 
                        ", " + str(item_id) + ")")
    try:
        cursor.execute(insert_auction_item)
    except mysql.connector.Error as err:
        raise Exception(err)
    return auction_id

def place_bid(cursor, auction_id: int, user_id: int, bid_amount: float, bid_time: datetime):
    insert_bid = ("INSERT INTO Bid (auction_id, user_id, bid_amount, bid_time) VALUES (" + 
                  str(auction_id) + ", " + str(user_id) + ", " + str(bid_amount) + ", '" + 
                  format_time(bid_time) + "')")
    try:
        cursor.execute(insert_bid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    return cursor.lastrowid

def get_auction_by_id(auction_id: int):
    select_statement = "SELECT * FROM {} WHERE auction_id = '" + str(auction_id) + "'"
    get_auction = select_statement.format("Auction")
    cursor.execute(get_auction)
    auction_info = cursor.fetchone()
    get_item = select_statement.format("AuctionItem")
    cursor.execute(get_item)
    item_id = cursor.fetchone()[1]
    auction = Auction(auction_info[0], item_id, auction_info[1],
                      auction_info[2], auction_info[3],
                      auction_info[4], auction_info[5],
                      auction_info[6], auction_info[7])
    print(auction)

if __name__ == '__main__':
    init_db()
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
	  host= db_host,
	  port = db_port,
	  user= db_user,
	  password= db_pwd,
	  database = "auction_db"
	)
    cursor = db.cursor()
    create_auction_tables(cursor)
    now = datetime.now()
    create_new_auction(cursor, now, now + timedelta(hours=2), 1, 5)
    create_new_auction(cursor, now + timedelta(hours=2), now + timedelta(hours=4), 4, 6)
    print_from_db(cursor, "Current auctions in Auction table:", "Auction")
    print_from_db(cursor, "Current auction-item relations in AuctionItem table:", "AuctionItem")
    place_bid(cursor, 1, 1, 20.50, now + timedelta(minutes=2))
    place_bid(cursor, 1, 2, 25.50, now + timedelta(minutes=3))
    place_bid(cursor, 1, 1, 30.50, now + timedelta(minutes=4))
    print_from_db(cursor, "Current bids in Bid table:", "Bid")
    get_auction_by_id(1)
    cursor.close()
	