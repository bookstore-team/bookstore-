import pytest

from fe.access.new_seller import register_new_seller
from fe.access import book
from fe.access import auth
from fe import conf

import uuid

class TestSearchExact:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.seller_id="test_point_search_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_point_search_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 1) #随机生成一本书，开店后加入
        for bk in self.books:
            self.title=bk.title
            self.author=bk.author
            code = self.seller.add_book(self.store_id, 0, bk)
            assert code == 200 

        yield

    def test_point_global_search_title(self):
        code=self.auth.search_title(self.title,None)
        assert code==200

    def test_point_global_search_author(self):
        code=self.auth.search_author(self.author,None)
        assert code==200     

    def test_point_instore_search_title(self):
        code=self.auth.search_title(self.title,self.store_id)
        assert code==200  

    def test_point_instore_search_author(self):
        code=self.auth.search_author(self.author,self.store_id)
        assert code==200       

    def test_not_exist_title(self):
        #店内搜索
        code=self.auth.search_title("xxxxxxxx",self.store_id)
        assert code!=200 #code==524
        
        #全局搜索
        code=self.auth.search_title("xxxxxxxx",None)
        assert code!=200 #code==524

    def test_not_exist_author(self):
        #店内搜索
        code=self.auth.search_author("xxxxxxxx",self.store_id)
        assert code!=200 #code==525
        
        #全局搜索
        code=self.auth.search_author("xxxxxxxx",None)
        assert code!=200 #code==525

