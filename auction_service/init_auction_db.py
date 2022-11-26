from flaskr.accessor.auction_accessor import AuctionAccessor

if __name__ == '__main__':
    accessor = AuctionAccessor()
    accessor.init_db()
    accessor.create_auction_tables()
    # The following line creates some test values for auctions and bids
    # Comment it out to just create the db and tables
    # accessor.db_test()
	