import mysql.connector
from datetime import datetime, timedelta

from common import local_config, docker_config

class DBInit():
    def __init__(self) -> None:
        # self.config = local_config
        self.config = docker_config

    def db_init(self) -> None:
        db_host = self.config.get('db_host')
        db_port = self.config.get('db_port')
        db_user = self.config.get('db_user')
        db_pwd = self.config.get('db_pwd')
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

        # create tables
        db = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pwd,
            database=self.config.get("db_name")
        )  
        cursor = db.cursor()
        # user_item
        cursor.execute("DROP TABLE IF EXISTS user_item")
        create_user_item = "CREATE TABLE user_item (user_id varchar(255), item_id int, UNIQUE KEY user_item_id (user_id, item_id))"
        cursor.execute(create_user_item)
        db.commit()

        # cart 
        cursor.execute("DROP TABLE IF EXISTS cart")
        create_cart = "CREATE TABLE cart (cart_id int AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), create_at datetime, checkout_at datetime)"
        cursor.execute(create_cart)
        db.commit()

        # cart item
        cursor.execute("DROP TABLE IF EXISTS cart_item")
        create_cart_item = "CREATE TABLE cart_item (cart_id int, item_id int, quantity int)"
        cursor.execute(create_cart_item)
        db.commit()

        # watchlist
        cursor.execute("DROP TABLE IF EXISTS watch_list")
        create_watch_list = "CREATE TABLE watch_list (id int AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), category_id int, max_price float)"
        cursor.execute(create_watch_list)
        db.commit()

        cursor.close()