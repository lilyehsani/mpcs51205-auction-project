import mysql.connector
from datetime import datetime, timedelta

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3308,
    'user': 'root',
    'password': 'root_password',
}

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

def create_auction_table():
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
    create_auction = "CREATE TABLE Auction (auction_id int, start_time datetime, end_time datetime, quantity int, status int, current_highest_bid int, finished_price float, finished_user int)"
    # create_auction = "CREATE TABLE Auction (auction_id int, quantity int, status int, current_highest_bid int, finished_price float, finished_user int)"
    cursor.execute("DROP TABLE IF EXISTS Auction")
    cursor.execute(create_auction)
    start_time_abc = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time_abc = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    insert_test_auction = "INSERT INTO Auction values (1234, '" + start_time_abc + "', '" + end_time_abc + "', 1, 0, 0, 0.0, 0)"
    # test creating tables
    cursor.execute(insert_test_auction)
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
    # test insert and read data
    cursor.execute("SELECT * FROM Auction")
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()

if __name__ == '__main__':
    init_db()
    create_auction_table()
	