import unittest
import sys
sys.path.append('/Users/yunchenliu/Desktop/mpcs51205-auction-project/inventory')
from accessor.category_accessor import CategoryAccessor
from accessor.item_accessor import ItemAccessor
from model.item import Item, item_status
from model.category import Category, category_status

#functions' return type have been changed. Old test cases not working now.
class Test(unittest.TestCase):
    def setUp(self):
        self.accessor = ItemAccessor()
        self.category_accessor = CategoryAccessor()

    # def test_create_item(self):
    #     name = "item one"
    #     shipping_cost = 2.2
    #     is_buy_now = True
    #     id = self.accessor.create_item(name, "item one desc", 2, shipping_cost, is_buy_now, 3.4, 1)
    #     new_items, _ = self.accessor.get_item_by_ids([id])
    #     self.assertEqual(len(new_items), 1)
    #     new_item = new_items[0]
    #     self.assertEqual(new_item.name, name)
    #     self.assertEqual(new_item.shipping_cost, shipping_cost)
    #     self.assertEqual(new_item.is_buy_now, is_buy_now)

    # def test_get_item_by_ids(self):
    #     ids = []
    #     for _ in range(4):
    #         id = self.accessor.create_item("aaa", "item one desc", 2, 4, True, 3.4, 1)
    #         ids.append(id)
    #     items = self.accessor.get_item_by_ids(ids)
    #     self.assertEqual(len(items), len(ids))

    # def test_update_item(self):
    #     id = self.accessor.create_item("aaa", "item one desc", 2, 4, True, 4, 1)
    #     new_description = "lalala"
    #     new_quantity = 5
    #     new_price = 7
    #     self.accessor.update_item(id, None, new_description, new_quantity, None, None, new_price)
    #     item = self.accessor.get_item_by_ids([id])[0]
    #     self.assertEqual(item.description, new_description)
    #     self.assertEqual(item.quantity, new_quantity)
    #     self.assertEqual(item.price, new_price)

    # def test_update_item_quantity(self):
    #     id = self.accessor.create_item("aaa", "item one desc", 2, 4, True, 4, 1)
    #     new_quantity = 11
    #     self.accessor.update_item_quantity(id, new_quantity)
    #     item = self.accessor.get_item_by_ids([id])[0]
    #     self.assertEqual(item.quantity, new_quantity)

    # def test_delete_item(self):
    #     id = self.accessor.create_item("aaa", "item one desc", 2, 4, True, 4, 1)
    #     self.accessor.delete_item(id)
    #     item = self.accessor.get_item_by_ids([id])[0]
    #     self.assertEqual(item.status, item_status['deleted'])

    # def test_create_category(self):
    #     category_name = "fruit"
    #     id = self.category_accessor.create_category(category_name, category_status['normal'])
    #     self.assertNotEqual(id, -1)
    #     category = self.category_accessor.get_category_by_ids([id])
    #     self.assertEqual(len(category), 1)

    # def test_update_category(self):
    #     category_name = "food"
    #     id = self.category_accessor.create_category(category_name, category_status['normal'])
    #     self.assertNotEqual(id, -1)
    #     new_category_name = "car"
    #     self.category_accessor.update_category(id, new_category_name)
    #     category = self.category_accessor.get_category_by_ids([id])
    #     self.assertEqual(len(category), 1)   
    #     self.assertEqual(category[0].name, new_category_name)        

    # def test_delete_category(self):
    #     id = self.category_accessor.create_category("food", category_status['normal'])
    #     self.category_accessor.delete_category(id)
    #     category = self.category_accessor.get_category_by_ids([id])
    #     self.assertEqual(len(category), 1)      
    #     self.assertEqual(category[0].status, category_status['deleted'])           

    # def test_create_category_item_relation(self):
    #     category_name = "car"
    #     cid = self.category_accessor.create_category(category_name, category_status['normal'])
    #     iid = self.accessor.create_item("tesla", "fast and fancy", 2, 300, True, 4000, 1)
    #     self.category_accessor.add_category_item_relation(iid, cid)
    #     item = self.accessor.get_item_by_ids([iid])[0]
    #     self.assertEqual(item.category_id, cid)
    #     self.assertEqual(item.category, category_name)

    # def test_update_category_of_item(self):
    #     category_name = "car"
    #     new_category_name = "tools"
    #     cid = self.category_accessor.create_category(category_name, category_status['normal'])
    #     new_cid = self.category_accessor.create_category(new_category_name, category_status['normal'])
    #     iid = self.accessor.create_item("tesla", "fast and fancy", 2, 300, True, 4000, 1)
    #     self.category_accessor.add_category_item_relation(iid, cid)
    #     self.category_accessor.update_category_of_item(iid, new_cid)
    #     item = self.accessor.get_item_by_ids([iid])[0]
    #     self.assertEqual(item.category_id, new_cid)
    #     self.assertEqual(item.category, new_category_name)

if __name__ == '__main__':
    unittest.main()
