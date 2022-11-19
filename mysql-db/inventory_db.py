import mysql.connector

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3309,
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
    cursor.execute("DROP DATABASE IF EXISTS inventory_db")
    cursor.execute("CREATE DATABASE inventory_db")
    cursor.close()


# Items user has for sale
def create_item_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="inventory_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS item")
    create_item = "CREATE TABLE item (item_id int, name varchar(255), description varchar(255), quantity int, " \
                  "shipping_cost float, is_buy_now boolean, purchasing_price float, status int) "
    cursor.execute(create_item)
    insert_item = "INSERT INTO item values (1, 'Bubble Tea', 'Watermelon jasmine flavor', 1, 3.0, false, 6.8, 0)"
    cursor.execute(insert_item)

    # test
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
    cursor.execute("SELECT * FROM item")
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()


# Items user has to buy
def create_category_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="inventory_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS categories")
    create_categories = "CREATE TABLE categories (category_id int, name varchar(255))"
    cursor.execute(create_categories)

    insert_categories = "INSERT INTO categories values (1, 'Food')"
    cursor.execute(insert_categories)

    # test
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
    cursor.execute("SELECT * FROM categories")
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()


def create_category_item_table():
    db_host = config.get('host')
    db_port = config.get('port')
    db_user = config.get('user')
    db_pwd = config.get('password')
    db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="inventory_db"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS category_item")
    create_category_item = "CREATE TABLE category_item (category_id int, item_id int)"
    cursor.execute(create_category_item)

    insert_category_item = "INSERT INTO category_item values (1, 1)"
    cursor.execute(insert_category_item)

    # test
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
    cursor.execute("SELECT * FROM category_item")
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()


if __name__ == '__main__':
    init_db()
    create_item_table()
    create_category_table()
    create_category_item_table()