import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer

from fe.access.book import Book
import uuid

class TestCancelOrder:
    @pytest.fixture(autouse=True)## 对给定测试执行给定的 fixtures,用例前置 & 参数化
    #当我们设置autouse参数为True时，默认测试作用域fixture内的测试函数都会全部执行
    def pre_run_initialization(self):
        self.seller_id = "test_cancel_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_cancel_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_cancel_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller=self.gen_book.seller

        yield

    #检查请求退款的用户是否有退款资格
    def test_authorization_error(self):
        #随机生成一个书单
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        assert ok
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list) #status:0(已下单未付款)
        assert code == 200

        self.password = self.password + "_x"
        code = self.buyer.cancel_order(self.buyer_id,self.password,self.order_id) 
        assert code != 200

    ##未付款买家申请取消
    def test_cancel_before_payment(self):
        #随机生成一个书单
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        assert ok
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list) #status:0(已下单未付款)
        assert code == 200

        #未付款买家申请取消
        code=self.buyer.cancel_order(self.buyer_id,self.password,self.order_id) 
        code==200

    ##付款但未发货，买家申请取消
    def test_cancel_after_payment_before_dispatch(self):
        #随机生成一个书单
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        assert ok
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list) #status:0(已下单未付款)
        assert code == 200
        buy_book_info_list = self.gen_book.buy_book_info_list
        
        self.total_price = 0
        for item in buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        
        code=self.buyer.add_funds(self.total_price)
        assert code==200
        code=self.buyer.payment(self.order_id) #status:1(已付款未发货)
        assert code==200
        code=self.buyer.cancel_order(self.buyer_id,self.password,self.order_id)
        assert code==200
    
    ##已发货但未收货，买家申请取消
    def test_cancel_after_dispatch_before_receiver(self):
        #随机生成一个书单
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        assert ok
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list) #status:0(已下单未付款)
        assert code == 200
        buy_book_info_list = self.gen_book.buy_book_info_list

        total_price = 0
        for item in buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                total_price = total_price + book.price * num
        code = self.buyer.add_funds(total_price)
        assert code == 200
        code = self.buyer.payment(self.order_id) #status:1(已付款未发货)
        assert code == 200
        code = self.seller.send_stock(self.seller_id,self.order_id) #status:2(已发货未收货)
        assert code ==200
        code=self.buyer.cancel_order(self.buyer_id,self.password,self.order_id)
        assert code!=200 #code==522
    


