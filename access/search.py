import requests
from urllib.parse import urljoin

class Search:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "search/")
        
    def param_search(self, title=None, author=None, tag=None, store_id=None) -> int:
        json = {
            "title": title, 
            "author": author, 
            "tag": tag, 
            "store_id": store_id
        }
        url = urljoin(self.url_prefix, "param_search")
        r = requests.post(url, json=json)
        return r.status_code

    # def content_search(self, content: str, store_id=None):
    #     json = {"content": content, "store_id": store_id}
    #     url = urljoin(self.url_prefix, "content_search")
    #     r = requests.post(url, json=json)
    #     return r.status_code
    