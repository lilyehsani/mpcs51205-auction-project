import mysql.connector
from datetime import datetime, timedelta

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'root_password',
}


def init_db():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd
    )
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS shopping_db")
    cursor.execute("CREATE DATABASE shopping_db")
    cursor.close()


# Items user has for sale
def create_user_item_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="shopping_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS user_item")
    create_user_item = "CREATE TABLE user_item (user_id int, item_id int)"
    cursor.execute(create_user_item)
    insert_user_item = "INSERT INTO user_item values (1, 1)"
    cursor.execute(insert_user_item)

    db.commit()
    cursor.close()


# Items user has to buy
def create_cart_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="shopping_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS cart")
    create_cart = "CREATE TABLE cart (cart_id int AUTO_INCREMENT PRIMARY KEY, user_id int, create_at datetime, checkout_at datetime)"
    cursor.execute(create_cart)

    start_time_test = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time_test = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    insert_cart = "INSERT INTO cart values (1, 1, '" + start_time_test + "', '" + end_time_test + "')"
    cursor.execute(insert_cart)

    db.commit()
    cursor.close()


def create_cart_item_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="shopping_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS cart_item")
    create_cart_item = "CREATE TABLE cart_item (cart_id int, item_id int)"
    cursor.execute(create_cart_item)

    insert_cart_item = "INSERT INTO cart_item values (1, 1)"
    cursor.execute(insert_cart_item)

    db.commit()
    cursor.close()


def db_test():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="shopping_db"
    )
    cursor = db.cursor()

    cursor.execute("SHOW TABLES")
    tables = []
    for x in cursor:
        table_name = x[0]
        tables.append(table_name)

    for table in tables:
        print(table + " table:")
        cursor.execute("SELECT * FROM " + table)
        results = cursor.fetchall()
        for result in results:
            print(result)

    cursor.close()


if __name__ == '__main__':
    init_db()
    create_user_item_table()
    create_cart_table()
    create_cart_item_table()
    db_test()
