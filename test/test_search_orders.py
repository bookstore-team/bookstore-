import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid

class TestSearchOrders:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200


    def test_ok(self):  #正常查询到
        code = self.buyer.search_orders(self.buyer_id,self.password)
        assert code == 200

    def test_error_authorization_id(self):  #由于buyer_id有错验证错误
        code=self.buyer.search_orders(self.buyer_id+"_x",self.password)
        assert code != 200

    def test_authorization_password(self):  #由于buyer_password有错验证错误
        code=self.buyer.search_orders(self.buyer_id,self.password+"_x")
        assert code != 200
    


