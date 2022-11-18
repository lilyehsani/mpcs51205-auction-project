import mysql.connector
from datetime import datetime, timedelta

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3308,
    'user': 'root',
    'password': 'root_password',
}

def print_auctions(cursor):
    print("Current auctions in Auction table:")
    cursor.execute("SELECT * FROM Auction")
    results = cursor.fetchall()
    for result in results:
        print(result)

def print_auction_items(cursor):
    print("Current auction-items in AuctionItem table:")
    cursor.execute("SELECT * FROM AuctionItem")
    results = cursor.fetchall()
    for result in results:
        print(result)

def print_bids(cursor):
    print("Current bids in Bid table:")
    cursor.execute("SELECT * FROM Bid")
    results = cursor.fetchall()
    for result in results:
        print(result)

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

    # Enter some test values into the tables
    insert_test_auction_item = "INSERT INTO AuctionItem values (1, 5)"
    bid_time = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
    insert_test_bid = ("INSERT INTO Bid (auction_id, user_id, bid_amount, bid_time) " +
                       "VALUES (1, 6, 20.50, '" + bid_time + "')")

    # Test creating tables
    cursor.execute(insert_test_auction_item)
    cursor.execute(insert_test_bid)
    cursor.execute("SHOW TABLES")
    print("Current tables in auction_db:")
    for x in cursor:
        print(x)

    # Test insert and read data
    print_auctions(cursor)
    print_auction_items(cursor)
    print_bids(cursor)

def create_new_auction(cursor, start_time: datetime, end_time: datetime, quantity: int, item_id: int):
    insert_auction = ("INSERT INTO Auction (start_time, end_time, quantity, status, " + 
                      "current_highest_bid, finished_price, finished_user) VALUES ('" + 
                      start_time.strftime('%Y-%m-%d %H:%M:%S') + "', '" + 
                      end_time.strftime('%Y-%m-%d %H:%M:%S') + 
                      "', " + str(quantity) + ", 0, null, null, null)")
    cursor.execute(insert_auction)
    auction_id = cursor.lastrowid
    insert_auction_item = ("INSERT INTO AuctionItem values (" + str(auction_id) + 
                           ", " + str(item_id) + ")")
    cursor.execute(insert_auction_item)
    return auction_id


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
    print(create_new_auction(cursor, now, now + timedelta(hours=2), 1, 5))
    print(create_new_auction(cursor, now + timedelta(hours=2), now + timedelta(hours=4), 4, 6))
    print_auctions(cursor)
    print_auction_items(cursor)
    cursor.close()
	