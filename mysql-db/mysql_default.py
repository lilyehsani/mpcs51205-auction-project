import mysql.connector

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'root_password',
}


def connect_mysql():
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
	cursor.execute("DROP DATABASE IF EXISTS auctiondb")
	cursor.execute("CREATE DATABASE auctiondb")
	cursor.close()
	db = mysql.connector.connect(
	  host= db_host,
	  port = db_port,
	  user= db_user,
	  password= db_pwd,
	  database = "auctiondb"
	)
	cursor = db.cursor()
	create_user_item_sql = "CREATE TABLE UserItem (UserID int,ItemID int)"
	create_categories_sql = "CREATE TABLE Categories (categoryID int, name varchar(255))"
	create_categories_item_sql = "CREATE TABLE CategoriesItem (categoryID int, ItemID int)"
	cursor.execute("DROP TABLE IF EXISTS UserItem")
	cursor.execute(create_user_item_sql)
	cursor.execute("DROP TABLE IF EXISTS Categories")
	cursor.execute(create_categories_sql)
	cursor.execute("DROP TABLE IF EXISTS CategoriesItem")
	cursor.execute(create_categories_item_sql)
	insert_user_item_sql = "insert into UserItem values (1234, 6789)"
	# test creating tables
	cursor.execute("SHOW TABLES")
	for x in cursor:
	  print(x)
	# test insert and read data
	cursor.execute(insert_user_item_sql)
	cursor.execute("SELECT * FROM UserItem")
	results = cursor.fetchall()
	for result in results:
		print(result)
	cursor.close()

if __name__ == '__main__':
	connect_mysql()
	