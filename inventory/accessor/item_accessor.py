import mysql.connector
from model.item import Item, item_status
from model.category import Category,category_status
from common import err_msg

class ItemAccessor:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(user='root', password='root_password', database='inventory_db', host='inventorydb', port=3306)
        # self.db = mysql.connector.connect(user='root', password='root_password', database='inventory_db', port=3309)
        self.cursor = self.db.cursor()

    def pack_item(self, rows):
        result = []
        try:
            for row in rows:
                # filter not normal items
                if row[7] != item_status['normal']:
                    continue
                result.append(Item(id = row[0],name=row[1],description=row[2], quantity=row[3],shipping_cost=row[4],is_buy_now=row[5],price=row[6],status = row[7], category_id=row[8], category=row[9]))
        except Exception as e:
            print(e)
            return [], err_msg["pack_failed"] 
        return result, None

    def check_item_exist(self, id) -> bool:
        ret, _ = self.get_item_by_ids([id])
        return len(ret) == 1

    def create_item(self, name:str, description:str, quantity:int, shipping_cost:float, is_buy_now:bool, price:float, status:int):
        sql = "insert into item values (NULL, '%s', '%s', %d, %f, %d, %f, %d)" % (name, description, quantity, shipping_cost, is_buy_now, price, status)
        try:
            self.cursor.execute(sql)
            ret_id = int(self.cursor.lastrowid)
            self.db.commit()
            return ret_id, None
        except Exception as e:
            print("create_item err", e)
            return -1, err_msg["db_err"]

    def get_item_by_ids(self, item_id_list):
        if len(item_id_list) == 0:
            return [], err_msg["param_err"]
        item_id_list = [str(i) for i in item_id_list] 
        id_list = ",".join(item_id_list)
        # sql = "SELECT * FROM item where item_id in (%s)" % (id_list)
        sql = "SELECT i.item_id, i.name,i.description, i.quantity, i.shipping_cost, i.is_buy_now, i.purchasing_price, i.status, categories.category_id, categories.name FROM item as i left join category_item on i.item_id = category_item.item_id left join categories on categories.category_id = category_item.category_id where i.item_id in (%s)"  % (id_list)
        print(sql)
        try:
            self.cursor.execute(sql)
            items = self.cursor.fetchall()
            if len(items) == 0:
                return [], err_msg["item_not_found"]
            return self.pack_item(items)
        except Exception as e:
            print("get_item_by_ids err", e)
            return [], err_msg['db_err']

    def get_red_flag_items(self):
        sql = "select i.item_id, i.name,i.description, i.quantity, i.shipping_cost, i.is_buy_now, i.purchasing_price, i.status, categories.category_id, categories.name FROM item as i left join category_item on i.item_id = category_item.item_id left join categories on categories.category_id = category_item.category_id where i.status = %d" % (item_status['red_flag'])
        try:
            self.cursor.execute(sql)
            items = self.cursor.fetchall()
            return self.pack_item(items)
        except Exception as e:
            print("get_red_flag_items err", e)
            return [], err_msg["db_err"]

    def change_item_status(self, id, status):
        return self.update_item(id=id, status=status)

    def update_item_quantity(self, id:int, quantity:int):
        return self.update_item(id, None, None, quantity)    

    def update_item(self, id:int, name:str=None, description:str=None, quantity:int=None, shipping_cost:float=None, is_buy_now:bool=None, price:float=None, status:int=None):
        if not self.check_item_exist(id):
            return False, err_msg["item_not_found"]
        sql = "update item set"
        if name:
            sql += " name = '%s'," %(name)
        if description:
            sql += " description = '%s'," %(description)
        if quantity and quantity >= 0:
            sql += " quantity = %d," %(quantity)
        if shipping_cost and shipping_cost >= 0:
            sql += " shipping_cost = %f," % (shipping_cost)
        if is_buy_now:
            sql += " is_buy_now = %d," % (is_buy_now)
        if price:
            sql += " purchasing_price = %f," % (price)
        if status:
            sql += " status = %d," % (status)
        sql = sql[:len(sql) - 1]
        sql += " where item_id = %d" % (id)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("inventory update_item error", e)
            return False, sql
        return True, None     

    def search_item_by_category(self, category_id):
        sql = "SELECT i.item_id, i.name,i.description, i.quantity, i.shipping_cost, i.is_buy_now, i.purchasing_price, i.status, categories.category_id, categories.name FROM item as i join category_item on i.item_id = category_item.item_id join categories on categories.category_id = category_item.category_id where categories.category_id = %d"  % (category_id) 
        try:
            self.cursor.execute(sql)
            items = self.cursor.fetchall()
            return self.pack_item(items)
        except Exception as e:
            print("inventory search_item_by_category error", e)
            return [], err_msg["db_err"]

    # search by name or description
    def search_item_by_key_words(self, key_word):
        sql = "select item_id from item where name like '%%%s%%' or description like '%%%s%%'" % (key_word, key_word)
        try:
            self.cursor.execute(sql)
            item_ids = self.cursor.fetchall()
            if len(item_ids) == 0:
                return [], None
            item_id_list = [i[0] for i in item_ids]
        except Exception as e:
            print("inventory search_item_by_category error", e)
            return [], err_msg["db_err"]  
        return self.get_item_by_ids(item_id_list)