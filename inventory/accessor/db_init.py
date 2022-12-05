import mysql.connector

class DBInit():
    def __init__(self) -> None:
        self.config = {
            # 'host': 'localhost',
            'host':'inventorydb',
            # 'port': 3309,
            'port':3306,
            'user': 'root',
            'password': 'root_password',
        }
        
    def db_init(self) -> None:
        #init database
        db_host = self.config.get('host')
        db_port = self.config.get('port')
        db_user = self.config.get('user')
        db_pwd = self.config.get('password')
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

        #create tables
        db = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pwd,
        database="inventory_db"
    )
        cursor = db.cursor()
        # item
        cursor.execute("DROP TABLE IF EXISTS item")
        create_item = "CREATE TABLE item (item_id int AUTO_INCREMENT PRIMARY KEY, name varchar(255), description varchar(255), quantity int, " \
                    "shipping_cost float, is_buy_now boolean, purchasing_price float, status int) "
        cursor.execute(create_item)
        db.commit()
        # categories
        cursor.execute("DROP TABLE IF EXISTS categories")
        create_categories = "CREATE TABLE categories (category_id int AUTO_INCREMENT PRIMARY KEY, name varchar(255), status int)"
        cursor.execute(create_categories)
        insert_categories = "INSERT INTO categories values (1, 'default', 0)"
        cursor.execute(insert_categories)
        db.commit()
        # category_item
        cursor.execute("DROP TABLE IF EXISTS category_item")
        create_category_item = "CREATE TABLE category_item (category_id int, item_id int, FOREIGN KEY (category_id) REFERENCES categories(category_id), FOREIGN KEY (item_id) REFERENCES item(item_id), UNIQUE KEY category_item_id (category_id, item_id))"
        cursor.execute(create_category_item)
        db.commit()
        cursor.close()