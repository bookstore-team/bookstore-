import pytest
import time
from fe.access import search
from fe.access import book
from fe import conf

class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.title = "平凡的世界"
        # self.store_id = "store_s_1_1_360cf0ce-7459-11ed-8d67-acde48001122"
        self.author = "路遥"
        self.tag = "小说"
        self.content = "狂人日记 & 孔乙己"
        self.mysearch = search.Search(conf.URL)
        yield
        # do after test

    # def test_param_ok(self):
    #     code = self.mysearch.param_search(title=self.title, author=self.author, tags=self.tags)
    #     assert code == 200

    #     code = self.mysearch.param_search(title=self.title, author=self.author, tags=self.tags, store_id=self.store_id)
    #     assert code == 200

    # def test_content_ok(self):
    #     code = self.mysearch.content_search(sub_content=self.subcontent)
    #     assert code == 200

    #     code = self.mysearch.content_search(sub_content=self.subcontent, store_id=self.store_id)
    #     assert code == 200
    

        
    def test_param_ok(self):
        code = self.mysearch.param_search(self.title, self.author, self.tag)
        assert code == 200

        # code = self.mysearch.param_search(self.title, self.author, self.tag, self.store_id)
        # assert code == 200

    # def test_content_ok(self):
    #     code = self.mysearch.content_search(self.content)
    #     assert code == 200

        # code = self.mysearch.content_search(self.content, self.store_id)
        # assert code == 200