import mysql.connector
from datetime import datetime
from common import local_config, docker_config

class ShoppingAccessor:
    def __init__(self):
        config = local_config
        # config = docker_config
        db_connection = mysql.connector.connect(
            host=config["db_host"],
            port=config["db_port"],
            user=config["db_user"],
            password=config["db_pwd"],
            database=config["db_name"] 
        )
        self.db = db_connection
        self.cursor = db_connection.cursor()


    '''
    - create item for sale
    Inventory service is responsible to update item table and category table
    Shopping Service only updates user-item table
    '''
    def add_user_item(self, user_id, item_id):
        query = "INSERT INTO user_item (user_id, item_id) VALUES (" + str(user_id) + "," + str(item_id) + ")"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)

    def get_current_cart(self, user_id):
        query = "SELECT * FROM cart WHERE user_id = " + str(user_id)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            raise Exception(err)
        carts = self.cursor.fetchall()
        if len(carts) == 0:
            cart_id = self.create_cart(user_id)
        else:
            cart_id = carts[-1][0]
            checkout_time = carts[-1][-1]
            if checkout_time is None or checkout_time < datetime.now():
                cart_id = self.create_cart(user_id)
        return cart_id

    def create_cart(self, user_id):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO cart (user_id, create_at) VALUES (" + str(user_id) + ", '" + current_time + "')"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)
        # get this cart id by iterating again
        query = "SELECT * FROM cart WHERE user_id = " + str(user_id)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            raise Exception(err)
        carts = self.cursor.fetchall()
        cart_id = carts[-1][0]
        return cart_id

    def add_item_to_cart(self, cart_id, item_id, quantity):
        # update cart item table
        query = "INSERT INTO cart_item (cart_id, item_id, quantity) VALUES (" + str(cart_id) + "," + str(item_id) + "," + str(quantity) + ")"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)

    def get_items_from_cart(self, cart_id):
        query = "SELECT * FROM cart_item WHERE cart_id = " + str(cart_id)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            raise Exception(err)
        items = self.cursor.fetchall()
        return items

    def checkout_items(self, cart_id, checkout_time):
        # add checkout_time to cart
        query = "UPDATE cart SET checkout_at = '" + checkout_time + "' WHERE cart_id = " + str(cart_id)
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)

    def remove_item_from_cart(self, cart_id, item_id):
        query = "DELETE FROM cart_item WHERE cart_id = " + str(cart_id) + " AND item_id = " + str(item_id)
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)

    # remove item for sale
    def remove_user_item(self, user_id, item_id):
        query = "DELETE FROM user_item WHERE user_id = " + str(user_id) + " AND item_id = " + str(item_id)
        try:
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            raise Exception(err)

    def get_items_for_sale_by_user(self, user_id):
        query = "SELECT * FROM user_item WHERE user_id = " + str(user_id)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            raise Exception(err)
        items = self.cursor.fetchall()
        return items
