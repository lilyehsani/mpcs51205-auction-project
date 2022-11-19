import unittest
from accessor.auction_accessor import AuctionAccessor
from faker import Faker

class Test(unittest.TestCase):
    def setUp(self):
        self.account_accessor = AuctionAccessor()
        self.fake = Faker()

    def test_create_aucount(self):
        auction_id = self.auction_accessor.create_auction(self.fake.date_time(), 
                                                          self.fake.date_time(), 
                                                          self.fake.pyint(),
                                                          self.fake.pyint())
        self.assertEqual(self.account_accessor.hard_delete_user(user_id), 1)

    def test_get_account_by_id(self):
        name = self.fake.name()
        user_name = self.fake.name()
        user_password = self.fake.name()
        user_id = self.account_accessor.create_user(name, 1, "email@hotmail.com", "4.5",
                                                    user_name, user_password)
        user = self.account_accessor.get_user_by_id(user_id)
        self.assertEqual(user.name, name)
        self.account_accessor.hard_delete_user(user_id)

    def test_get_account_by_user_name_and_password(self):
        name = self.fake.name()
        user_name = self.fake.name()
        user_password = self.fake.name()
        user_id = self.account_accessor.create_user(name, 1, "email@hotmail.com", "4.5",
                                                    user_name, user_password)
        user = self.account_accessor.get_user(user_name, user_password)
        self.assertEqual(user.name, name)
        self.account_accessor.hard_delete_user(user_id)


if __name__ == '__main__':
    unittest.main()
