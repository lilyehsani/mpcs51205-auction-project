import mysql.connector
from datetime import datetime

db_host = "localhost"
db_port = 3307
db_user = "root"
db_pwd = "root_password"
db_name = "shopping_db"


class ShoppingAccessor:
    def __init__(self):
        db_connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pwd,
            database=db_name
        )
        self.db = db_connection
        self.cursor = db_connection.cursor()


    '''
    Inventory service is responsible to update item table and category table
    Shopping Service only updates user-item table
    '''
    def update_user_item(self, user_id, item_id):
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

    def add_item_to_cart(self, cart_id, item_id):
        # update cart item table
        query = "INSERT INTO cart_item (cart_id, item_id) VALUES (" + str(cart_id) + "," + str(item_id) + ")"
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
