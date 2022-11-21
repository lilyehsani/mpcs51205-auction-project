import mysql.connector
import sys
sys.path.append('/Users/yunchenliu/Desktop/mpcs51205-auction-project/inventory')
from model.item import Item, item_status
from model.category import Category,category_status

class CategoryAccessor:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(user='root', password='root_password', database='inventory_db', port=3309)
        self.cursor = self.db.cursor()

    def pack_category(self, rows):
        result = []
        for row in rows: 
            result.append(Category(id = row[0],name=row[1], status = row[2]))
        return result

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

    # update category for item
    # add category when getting items
    def add_category_item_relation(self, item_id, category_id):
        sql = "insert into category_item values (%d, %d)" % (category_id, item_id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            print("add_category_item_relation error ", e)
            return False

    def update_category_of_item(self, item_id, category_id):
        sql = "update category_item set category_id = %d where item_id = %d" % (category_id, item_id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            print("update_category_of_item error ", e)
            return False            

    def get_all_categories(self):
        sql = "select * from categories"
        try:
            self.cursor.execute(sql)
            categories = self.cursor.fetchall()
            return self.pack_category(categories) 
        except Exception as e:
            print("get_all_categories error ", e)
            return []    

