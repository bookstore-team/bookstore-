import pytest

#import sys 
#import os
#把当前文件所在文件夹的父文件夹路径加入到PY

#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fe.access.new_seller import register_new_seller
from fe.access import book
from fe.access import auth
from fe import conf

import uuid


class TestSearchInexact:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.seller_id= "test_search_inexact_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_inexact_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(5, 1) #随机生成一本书，开店后上架
        for bk in self.books:
            self.title=bk.title
            self.author=bk.author
            self.content=bk.content
            self.tags=bk.tags
            code = self.seller.add_book(self.store_id, 0, bk)
            assert code == 200 

        yield

    #全局搜索title，存在与该查询相关的书
    def test_inexact_global_search_title(self):
        search_key=self.title[6:8] #随机截取一个title字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_title_inexact(search_key,None)
        assert code==200
    
    #全局搜索author，存在查询相关的作者的作品
    def test_inexact_global_search_author(self):
        search_key=self.author[3:5] #随机截取一个author字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_author_inexact(search_key,None)
        assert code==200
    
    #全局搜索content，存在与该查询相关的书  
    def test_inexact_global_search_content(self):
        search_key=self.content[5:9] #随机截取一个content字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_content_inexact(search_key,None)
        assert code==200

    #全局搜索tag，存在与该查询相关的tag的书
    def test_inexact_global_search_tag(self):
        seacrh_key=self.tags[0][0:2] #随机截取一个tag字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_tag_inexact(seacrh_key,None)
        assert code==200

    #店内搜索title，存在该书
    def test_inexact_instore_search_title(self):
        search_key=self.title[6:8] #随机截取一个title字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_title_inexact(search_key,self.store_id)
        assert code==200  
    
    #店内搜索author，存在该作者
    def test_inexact_instore_search_author(self):
        search_key=self.author[3:5] #随机截取一个author字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_author_inexact(search_key,self.store_id)
        assert code==200       
    
    #店内搜索content，存在相关内容
    def test_inexact_instore_search_content(self):
        search_key=self.content[5:9] #随机截取一个content字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_content_inexact(search_key,self.store_id)
        assert code==200

    #店内搜索tag，存在相关内容
    def test_inexact_instore_search_tag(self):
        seacrh_key=self.tags[0][0:2] #随机截取一个tag字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_tag_inexact(seacrh_key,self.store_id)
        assert code==200

    #不存在该书
    def test_not_exist_title_inexact(self):
        #店内搜索
        code=self.auth.search_title_inexact("xxxxxxxx",self.store_id)
        assert code!=200 #code==524
        
        #全局搜索
        code=self.auth.search_title_inexact("xxxxxxxx",None)
        assert code!=200 #code==524
    
    #不存在该作者
    def test_not_exist_author_inexact(self):
        #店内搜索
        code=self.auth.search_author_inexact("xxxxxxxx",self.store_id)
        assert code!=200 #code==525
        
        #全局搜索
        code=self.auth.search_author_inexact("xxxxxxxx",None)
        assert code!=200 #code==525

    #不存在该tag
    def test_not_exist_tag_inexact(self):
        #店内搜索
        code=self.auth.search_tag_inexact("xxxxxxxx",self.store_id)
        assert code!=200 #code==526
        
        #全局搜索
        code=self.auth.search_tag_inexact("xxxxxxxx",None)
        assert code!=200 #code==526
    
    #不存在该content相关的内容
    def test_not_exist_content_inexact(self):
        #店内搜索
        code=self.auth.search_content_inexact("xxxxxxxx",self.store_id)
        assert code!=200 #code==527
        
        #全局搜索
        code=self.auth.search_content_inexact("xxxxxxxx",None)
        assert code!=200 #code==527
    
    #在全局搜索测试分页功能:用书名模糊搜索
    def test_page_global_search_with_title_inexact(self):
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 1) #随机生成一本书，开店后上架

        #一本书插入30次
        for i in range(30):
            #创建30个书店
            seller_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            store_id=str('test_page_global_inexact_search_store_id_'+str(uuid.uuid1()))
            password=seller_id
            seller = register_new_seller(seller_id, password)
            code = seller.create_store(store_id)
            assert code == 200

            for bk in self.books:
                self.title=bk.title
                self.author=bk.author
                code = seller.add_book(store_id, 0, bk)
                assert code == 200 

        search_key=self.title[6:8] #随机截取一个title字符串中的部分内容，以保证搜索的时候一定搜得到    
        code=self.auth.search_title_inexact(search_key,None)
        assert code==200
        
    #在全局搜索测试分页功能:用作者名模糊搜索
    def test_page_global_search_with_author_inexact(self):
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 1) #随机生成一本书，开店后上架

        #一本书插入30次
        for i in range(30):
            #创建30个书店
            seller_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            store_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            password=seller_id
            seller = register_new_seller(seller_id, password)
            code = seller.create_store(store_id)
            assert code == 200

            for bk in self.books:
                self.title=bk.title
                self.author=bk.author
                code = seller.add_book(store_id, 0, bk)
                assert code == 200 

        search_key=self.author[3:5] #随机截取一个author字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_author_inexact(search_key,None)
        assert code==200
        
    #在全局搜索测试分页功能:用content模糊搜索
    def test_page_global_search_with_content_inexact(self):
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 1) #随机生成一本书，开店后上架

        #一本书插入30次
        for i in range(30):
            #创建30个书店
            seller_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            store_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            password=seller_id
            seller = register_new_seller(seller_id, password)
            code = seller.create_store(store_id)
            assert code == 200

            for bk in self.books:
                self.title=bk.title
                self.author=bk.author
                code = seller.add_book(store_id, 0, bk)
                assert code == 200 
        search_key=self.content[5:9] #随机截取一个content字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_content_inexact(search_key,None)
        assert code==200

    #在全局搜索测试分页功能:用tag模糊搜索
    def test_page_global_search_with_tag_inexact(self):
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 1) #随机生成一本书，开店后上架

        #一本书插入30次
        for i in range(30):
            #创建30个书店
            seller_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            store_id=str('test_page_global_inexact_search_seller_id_'+str(uuid.uuid1()))
            password=seller_id
            seller = register_new_seller(seller_id, password)
            code = seller.create_store(store_id)
            assert code == 200

            for bk in self.books:
                self.title=bk.title
                self.author=bk.author
                code = seller.add_book(store_id, 0, bk)
                assert code == 200 
        seacrh_key=self.tags[0][0:2] #随机截取一个tag字符串中的部分内容，以保证搜索的时候一定搜得到
        code=self.auth.search_tag_inexact(seacrh_key,None)
        assert code==200

