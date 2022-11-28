import mysql.connector
from flaskr.model.auction import Auction
from flaskr.model.bid import Bid
from datetime import datetime, timedelta

class AuctionAccessor:
    '''
    Provides an interface for the Auction database. Assumes the database has been created, and its
    tables (Auction, AuctionItem, and Bid) have been set up.
    '''
    def __init__(self):
        self.db_host = "auction_db"
        self.db_port = 3306
        self.db_user = "root"
        self.db_pwd = "root_password"
        self.db_name = "auction_db"

    #-------- Printing Functions --------#
    def print_from_db(self, message: str, table_name: str):
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
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

    def print_tables(self):
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
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
    
    #-------- Initialization Functions --------#
    '''
    Initializes the database.
    '''
    def init_db(self):
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
        )
        cursor = db.cursor()

        # Create database
        cursor.execute("DROP DATABASE IF EXISTS auction_db")
        cursor.execute("CREATE DATABASE auction_db")

        # Commit changes and close
        db.commit()
        cursor.close()
        db.close()

    '''
    Creates the three auction-related tables we need: Auction, AuctionItem, and Bid.
    '''
    def create_auction_tables(self):
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        # Create 3 auction-related tables
        create_auction = ("CREATE TABLE Auction (auction_id INT AUTO_INCREMENT PRIMARY KEY, " + 
                        "start_time datetime, end_time datetime, start_price float, status int, " +
                        "current_highest_bid_id int, finished_price float, finished_user varchar(255))")
        create_auction_item = "CREATE TABLE AuctionItem (auction_id int, item_id int)"
        create_bids = ("CREATE TABLE Bid (bid_id INT AUTO_INCREMENT PRIMARY KEY, auction_id int, " +
                    "user_id varchar(255), bid_amount float, bid_time datetime)")
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

    #-------- Accessor Functions --------#
    def create_new_auction(self, start_time: datetime, end_time: datetime, start_price: float, item_id: int) -> int:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        # Insert the auction
        insert_auction = ("INSERT INTO Auction (start_time, end_time, start_price, status, " + 
                        "current_highest_bid_id, finished_price, finished_user) VALUES " + 
                        "(%s, %s, %s, %s, %s, %s, %s)")
        insert_auction_data = (start_time, end_time, start_price, 0, None, None, None)
        
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

    def update_auction(self, auction_id: int, field_name: str, new_value):
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
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

    def place_bid(self, auction_id: int, user_id: str, bid_amount: float, bid_time: datetime) -> int:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
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
        start_price = auction[3]
        status = auction[4]
        current_highest_bid_id = auction[5]
        
        # Cannot place bid if the auction is not online
        if status != 1:
            print(status)
            raise Exception("Auction is not online. Status={}".format(status))

        # Check current highest bid and ensure that new bid is higher
        if current_highest_bid_id is not None:
            get_bid = "SELECT * FROM Bid WHERE bid_id = %s"
            bid_data = [current_highest_bid_id]
            cursor.execute(get_bid, bid_data)
            bid = cursor.fetchone()
            current_highest_bid_amount = bid[3]
            if current_highest_bid_amount >= bid_amount:
                raise Exception("Bid is not higher than current highest bid.")
        else:
            # Check that the first bid is greater than or equal to starting price.
            if bid_amount < start_price:
                raise Exception("Bid is not higher than the starting price.")

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
        update_auction = "UPDATE Auction SET current_highest_bid_id = %s WHERE auction_id = %s"
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

    def get_auction_by_id(self, auction_id: int) -> Auction:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        select_statement = "SELECT * FROM {} WHERE auction_id = %s"
        get_auction = select_statement.format("Auction")
        get_auction_data = [auction_id]
        cursor.execute(get_auction, get_auction_data)
        auctions = cursor.fetchall()
        if len(auctions) < 1:
            raise Exception("Auction does not exist.")

        auction_info = auctions[0]

        get_auction_item = select_statement.format("AuctionItem")
        get_auction_item_data = [auction_id]
        cursor.execute(get_auction_item, get_auction_item_data)
        item_id = cursor.fetchone()[1]
        auction = Auction(auction_info[0], item_id, auction_info[1], auction_info[2], 
                          auction_info[3], auction_info[4], auction_info[5], 
                          auction_info[6], auction_info[7])
                        
        return auction

    def get_all_auction(self) -> list:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        get_auction = "SELECT * FROM Auction"
        cursor.execute(get_auction)
        fetched_auctions = cursor.fetchall()

        auctions = []

        for auction_info in fetched_auctions:
            auction_id = auction_info[0]
            get_auction_item = "SELECT * FROM AuctionItem WHERE auction_id = %s"
            get_auction_item_data = [auction_id]
            cursor.execute(get_auction_item, get_auction_item_data)
            item_id = cursor.fetchone()[1]
            auction = Auction(auction_id, item_id, auction_info[1], auction_info[2], 
                              auction_info[3], auction_info[4], auction_info[5], 
                              auction_info[6], auction_info[7])
            auctions.append(auction)

        return auctions

    def get_all_auction_by_status(self, status: int) -> list:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        get_auction = "SELECT * FROM Auction WHERE status = %s"
        get_auction_data = [status]
        cursor.execute(get_auction, get_auction_data)
        fetched_auctions = cursor.fetchall()

        auctions = []

        for auction_info in fetched_auctions:
            auction_id = auction_info[0]
            get_auction_item = "SELECT * FROM AuctionItem WHERE auction_id = %s"
            get_auction_item_data = [auction_id]
            cursor.execute(get_auction_item, get_auction_item_data)
            item_id = cursor.fetchone()[1]
            auction = Auction(auction_id, item_id, auction_info[1], auction_info[2], 
                              auction_info[3], auction_info[4], auction_info[5], 
                              auction_info[6], auction_info[7])
            auctions.append(auction)

        return auctions

    def get_bid_by_id(self, bid_id: int) -> Bid:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        get_bid = "SELECT * FROM Bid WHERE bid_id = %s"
        get_bid_data = [bid_id]
        cursor.execute(get_bid, get_bid_data)
        bids = cursor.fetchall()
        if len(bids) < 1:
            raise Exception("Bid {} does not exist.".format(bid_id))

        bid_info = bids[0]

        bid = Bid(bid_info[0], bid_info[1], bid_info[2], bid_info[3], bid_info[4])
                        
        return bid

    def get_bids_by_auction(self, auction_id: int) -> list:
        # Connect to db and acquire cursor
        db = mysql.connector.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_pwd,
            database = self.db_name,
        )
        cursor = db.cursor()

        get_bid = "SELECT * FROM Bid WHERE auction_id = %s"
        get_bid_data = [auction_id]
        cursor.execute(get_bid, get_bid_data)
        fetched_bids = cursor.fetchall()

        bids = []

        for bid_info in fetched_bids:
            bid = Bid(bid_info[0], bid_info[1], bid_info[2], bid_info[3], bid_info[4])
            bids.append(bid)
                        
        return bids

    def db_test(self):
        self.print_tables()
        now = datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        print((now + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'))
        auction_1 = self.create_new_auction(now, now + timedelta(hours=2), 1, 5)
        self.create_new_auction(now + timedelta(hours=2), now + timedelta(hours=4), 4, 6)
        self.print_from_db("Current auctions in Auction table:", "Auction")
        self.print_from_db("Current auction-item relations in AuctionItem table:", "AuctionItem")
        self.update_auction(auction_1, "status", 1)
        self.print_from_db("The first of the following auctions should now have status=1:", "Auction")
        self.place_bid(1, 1, 20.50, now + timedelta(minutes=2))
        self.place_bid(1, 2, 25.50, now + timedelta(minutes=3))
        self.place_bid(1, 1, 30.50, now + timedelta(minutes=4))
        try:
            self.place_bid(1, 2, 30.50, now + timedelta(minutes=4))
        except Exception as err:
            print("The following error should prevent the bid because it is too low:")
            print(err)
        try:
            self.place_bid(2, 1, 30.50, now + timedelta(minutes=4))
        except Exception as err:
            print("The follow error should prevent the bid because the auction is offline:")
            print(err)
        self.print_from_db("Current bids in Bid table:", "Bid")
    