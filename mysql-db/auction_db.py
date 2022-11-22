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
db_host = "localhost"
db_port = 3308
db_user = "root"
db_pwd = "root_password"
db_name = "auction_db"

def print_from_db(message: str, table_name: str):
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM " + table_name)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return

    # Print the provided message
    print(message)
    results = cursor.fetchall()
    for result in results:
        print(result)

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

def print_tables():
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    cursor.execute("SHOW TABLES")
    print("Current tables in auction_db:")
    for x in cursor:
        print(x)

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

def init_db():
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host= db_host,
        port = db_port,
        user= db_user,
        password= db_pwd
    )
    cursor = db.cursor()

    # Create database
    cursor.execute("DROP DATABASE IF EXISTS auction_db")
    cursor.execute("CREATE DATABASE auction_db")

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

def create_auction_tables():
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

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

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()


def create_new_auction(start_time: datetime, end_time: datetime, quantity: int, item_id: int):
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    # Insert the auction
    insert_auction = ("INSERT INTO Auction (start_time, end_time, quantity, status, " + 
                      "current_highest_bid, finished_price, finished_user) VALUES " + 
                      "(%s, %s, %s, %s, %s, %s, %s)")
    insert_auction_data = (start_time, end_time, quantity, 0, None, None, None)
    
    try:
        cursor.execute(insert_auction, insert_auction_data)
    except mysql.connector.Error as err:
        raise Exception(err)
    auction_id = cursor.lastrowid

    # Insert the auction-item
    insert_auction_item = "INSERT INTO AuctionItem values (%s, %s)"
    insert_auction_item_data = (auction_id, item_id)

    try:
        cursor.execute(insert_auction_item, insert_auction_item_data)
    except mysql.connector.Error as err:
        raise Exception(err)

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

    return auction_id


def update_auction(auction_id: int, field_name: str, new_value):
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    # Ensure the auction to be updated exists
    get_auction = "SELECT * FROM Auction WHERE auction_id = %s"
    get_auction_data = [auction_id]
    cursor.execute(get_auction, get_auction_data)
    auctions = cursor.fetchall()
    if len(auctions) < 1:
        raise Exception("Auction does not exist.")

    # Update status of the auction
    update_statement = "UPDATE Auction SET {} = %s WHERE auction_id = %s"
    update_auction = update_statement.format(field_name)
    update_auction_data = (new_value, auction_id)

    try:
        cursor.execute(update_auction, update_auction_data)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()


def place_bid(auction_id: int, user_id: int, bid_amount: float, bid_time: datetime):
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    # Get the auction that the bid is being placed on
    get_auction = "SELECT * FROM Auction WHERE auction_id = %s"
    get_auction_data = [auction_id]
    cursor.execute(get_auction, get_auction_data)
    auctions = cursor.fetchall()
    if len(auctions) < 1:
        raise Exception("Auction does not exist.")
    
    # Get each needed piece of auction informtion
    auction = auctions[0]
    auction_id = auction[0]
    status = auction[4]
    current_highest_bid_id = auction[5]
    
    # Cannot place bid if the auction is not online
    if status != 1:
        raise Exception("Auction is not online.")

    # Check current highest bid and ensure that new bid is higher
    if current_highest_bid_id is not None:
        get_bid = "SELECT * FROM Bid WHERE bid_id = %s"
        bid_data = [current_highest_bid_id]
        cursor.execute(get_bid, bid_data)
        bid = cursor.fetchone()
        current_highest_bid_amount = bid[3]
        if current_highest_bid_amount >= bid_amount:
            raise Exception("Bid is not higher than current highest bid.")

    # Insert bid
    insert_bid = ("INSERT INTO Bid (auction_id, user_id, bid_amount, bid_time) VALUES " + 
                  "(%s, %s, %s, %s)")
    insert_bid_data = (auction_id, user_id, bid_amount, bid_time)

    try:
        cursor.execute(insert_bid, insert_bid_data)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    new_highest_bid_id = cursor.lastrowid

    # Update current highest bid in Auction table
    update_auction = "UPDATE Auction SET current_highest_bid = %s WHERE auction_id = %s"
    update_auction_data = (new_highest_bid_id, auction_id)

    try:
        cursor.execute(update_auction, update_auction_data)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

    return cursor.lastrowid

def get_auction_by_id(auction_id: int):
    # Connect to db and acquire cursor
    db = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    cursor = db.cursor()

    select_statement = "SELECT * FROM {} WHERE auction_id = %s"
    get_auction = select_statement.format("Auction")
    get_auction_data = [auction_id]
    cursor.execute(get_auction, get_auction_data)
    auction_info = cursor.fetchone()
    get_auction_item = select_statement.format("AuctionItem")
    get_auction_item_data = [auction_id]
    cursor.execute(get_auction_item, get_auction_item_data)
    item_id = cursor.fetchone()[1]
    auction = Auction(auction_info[0], item_id, auction_info[1],
                      auction_info[2], auction_info[3],
                      auction_info[4], auction_info[5],
                      auction_info[6], auction_info[7])

    # Commit changes and close
    db.commit()
    cursor.close()
    db.close()

    return auction

def db_test():
    print_tables()
    now = datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    print((now + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'))
    auction_1 = create_new_auction(now, now + timedelta(hours=2), 1, 5)
    create_new_auction(now + timedelta(hours=2), now + timedelta(hours=4), 4, 6)
    print_from_db("Current auctions in Auction table:", "Auction")
    print_from_db("Current auction-item relations in AuctionItem table:", "AuctionItem")
    update_auction(auction_1, "status", 1)
    print_from_db("The first of the following auctions should now have status=1:", "Auction")
    place_bid(1, 1, 20.50, now + timedelta(minutes=2))
    place_bid(1, 2, 25.50, now + timedelta(minutes=3))
    place_bid(1, 1, 30.50, now + timedelta(minutes=4))
    try:
        place_bid(1, 2, 30.50, now + timedelta(minutes=4))
    except Exception as err:
        print("The following error should prevent the bid because it is too low:")
        print(err)
    try:
        place_bid(2, 1, 30.50, now + timedelta(minutes=4))
    except Exception as err:
        print("The follow error should prevent the bid because the auction is offline:")
        print(err)
    print_from_db("Current bids in Bid table:", "Bid")
    print(get_auction_by_id(1))


if __name__ == '__main__':
    init_db()
    create_auction_tables()
    db_test()
	