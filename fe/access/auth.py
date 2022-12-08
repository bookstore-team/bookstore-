import requests
from urllib.parse import urljoin


class Auth:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")

    def login(self, user_id: str, password: str, terminal: str) -> (int, str):
        json = {"user_id": user_id, "password": password, "terminal": terminal}
        url = urljoin(self.url_prefix, "login")
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("token")

    def register(
        self,
        user_id: str,
        password: str
    ) -> int:
        json = {
            "user_id": user_id,
            "password": password
        }
        url = urljoin(self.url_prefix, "register")
        r = requests.post(url, json=json)
        return r.status_code

    def password(self, user_id: str, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "password")
        r = requests.post(url, json=json)
        return r.status_code

    def logout(self, user_id: str, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def unregister(self, user_id: str, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "unregister")
        r = requests.post(url, json=json)
        return r.status_code
     
    ### lsq:精确搜索title 
    def search_title(self,search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_title")

        r=requests.post(url,json=json)
        return r.status_code

    ### lsq:精确搜索author
    def search_author(self,search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_author")

        r=requests.post(url,json=json)
        return r.status_code

    ###lsq:模糊搜索title
    def search_title_inexact(self, search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_title_inexact")

        r=requests.post(url,json=json)
        return r.status_code

    ###lsq:模糊搜索author
    def search_author_inexact(self, search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_author_inexact")

        r=requests.post(url,json=json)
        return r.status_code

    ###lsq:模糊搜索tag
    def search_tag_inexact(self, search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_tag_inexact")

        r=requests.post(url,json=json)
        return r.status_code

    ###lsq:模糊搜索content
    def search_content_inexact(self, search_key:str,store_id:str):
        json={"search_key":search_key,"store_id":store_id}
        url = urljoin(self.url_prefix, "search_content_inexact")

        r=requests.post(url,json=json)
        return r.status_code