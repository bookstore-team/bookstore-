import pytest

from fe.access.new_seller import register_new_seller
from fe.access import book
import uuid

class TestSetBookPrice:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        #do before test
        self.user_id = "test_set_book_price_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_set_book_price_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        self.seller = register_new_seller(self.user_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 2)
        for bk in self.books:
            code = self.seller.add_book(self.store_id, 0, bk)
            assert code == 200        
        yield
        #do after test

    #正常改价
    def test_ok(self):
        for b in self.books:
            book_id=b.id
            code=self.seller.set_book_price(self.user_id,self.store_id,book_id,15)
            assert code==200

    #store_id不存在而无法改价
    def test_error_store_id(self):
        for b in self.books:
            book_id=b.id
            code = self.seller.set_book_price(self.user_id,self.store_id+"_x",book_id,15)
            assert code != 200

    #book_id不存在而无法改价
    def test_error_book_id(self):
        for b in self.books:
            book_id=b.id
            code = self.seller.set_book_price(self.user_id,self.store_id,book_id+"_x",15)
            assert code != 200

    #user_id不存在而无法改价
    def test_error_user_id(self):
        for b in self.books:
            book_id=b.id
            code = self.seller.set_book_price(self.user_id+"_x",self.store_id,book_id,15)
            assert code != 200