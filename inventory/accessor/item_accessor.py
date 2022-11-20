from unicodedata import name
import mysql.connector
# import model
import sys
sys.path.append('/Users/yunchenliu/Desktop/mpcs51205-auction-project/inventory')
from model.item import Item, item_status
from model.category import Category,category_status

class ItemAccessor:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(user='root', password='root_password', database='inventory_db', port=3309)
        self.cursor = self.db.cursor()

    def pack_item(self, rows) -> list[Item]:
        result = []
        for row in rows: 
            result.append(Item(id = row[0],name=row[1],description=row[2], quantity=row[3],shipping_cost=row[4],is_buy_now=row[5],price=row[6],status = row[7]))
        return result
    
    def pack_category(self, rows):
        result = []
        for row in rows: 
            result.append(Category(id = row[0],name=row[1], status = row[2]))
        return result

    def check_item_exist(self, id) -> bool:
        ret = self.get_item_by_ids([id])
        return len(ret) == 1

    def create_item(self, name:str, description:str, quantity:int, shipping_cost:float, is_buy_now:bool, price:float, status:int) -> int:
        sql = "insert into item values (NULL, '%s', '%s', %d, %f, %d, %f, %d)" % (name, description, quantity, shipping_cost, is_buy_now, price, status)
        self.cursor.execute(sql)
        ret_id = int(self.cursor.lastrowid)
        self.db.commit()
        return ret_id

    def get_item_by_ids(self, item_id_list: list[int]) -> Item:
        if len(item_id_list) == 0:
            return []
        item_id_list = [str(i) for i in item_id_list] 
        id_list = ",".join(item_id_list)
        sql = "SELECT * FROM item where item_id in (%s)" % (id_list)
        print(sql)
        self.cursor.execute(sql)
        items = self.cursor.fetchall()
        return self.pack_item(items)
    
    def delete_item(self, id:int) -> bool:
        self.update_item(id=id, status=item_status["deleted"])

    def update_item_quantity(self, id:int, quantity:int):
        self.update_item(id, None, None, quantity)    

    def update_item(self, id:int, name:str=None, description:str=None, quantity:int=None, shipping_cost:float=None, is_buy_now:bool=None, price:float=None, status:int=None) -> bool:
        if not self.check_item_exist(id):
            return False
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
            return False
        return True   

    def create_category(self, name:str, status:int) -> int:
        sql = "insert into categories values (NULL, '%s', %d)" % (name, status)
        print(sql)
        try:
            self.cursor.execute(sql)
            ret_id = int(self.cursor.lastrowid)
            self.db.commit()
            return ret_id    
        except Exception as e:
            print("create_category error:", e)
            return -1

    def get_category_by_ids(self, category_id_list:list[int]) -> list[Category]:
        if len(category_id_list) == 0:
            return []
        category_id_list = [str(i) for i in category_id_list] 
        id_list = ",".join(category_id_list)
        sql = "SELECT * FROM categories where category_id in (%s)" % (id_list)
        print(sql)
        self.cursor.execute(sql)
        categories = self.cursor.fetchall()
        return self.pack_category(categories) 

    def update_category(self, id, new_name):
        if len(self.get_category_by_ids([id])) != 1:
            return False
        sql = "update categories set name = '%s' where category_id = %d" % (new_name, id)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("inventory update_category error", e)
            return False
        return True  

    def delete_category(self, id):
        if len(self.get_category_by_ids([id])) != 1:
            return False
        sql = "update categories set status = %d where category_id = %d" % (category_status["deleted"], id)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("inventory delete_category error", e)
            return False
        return True  

    # add category when creating item
    # update category for item
    # add category when getting items

    def get_all_categories(self):
        pass

    def search_item_by_category(self, category):
        pass

    # search by name or description
    def search_item_by_key_words(self, key_words):




    

if __name__ == '__main__':
    ia = ItemAccessor()