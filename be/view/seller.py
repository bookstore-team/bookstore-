from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import seller
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    s = seller.Seller()
    code, message = s.create_store(user_id, store_id)
    return jsonify({"message": message}), code


@bp_seller.route("/add_book", methods=["POST"])
def seller_add_book():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_info: str = request.json.get("book_info")
    stock_level: str = request.json.get("stock_level", 0)
    title = book_info['title']      ####
    tag = str(book_info['tags'])    ####
    content = book_info['content']  ####
    author = book_info['author']    ####
    book_price=book_info['price']    ####
    s = seller.Seller()
    code, message = s.add_book(user_id=user_id, store_id=store_id, book_id=book_info.get("id"), book_json_str=json.dumps(book_info), stock_level=stock_level, title=title,
                               tag=tag, content=content, author=author,book_price=book_price)  ####
    return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_id: str = request.json.get("book_id")
    add_num: str = request.json.get("add_stock_level", 0)
    s = seller.Seller()
    code, message = s.add_stock_level(user_id, store_id, book_id, add_num)
    return jsonify({"message": message}), code

@bp_seller.route("/send_stock", methods=["POST"])#######CBY
def send_stock():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    s = seller.Seller()
    code, message = s.send_stock(user_id=user_id, order_id=order_id)
    return jsonify({"message": message}), code

#### lsq:新功能：卖家改价
@bp_seller.route("/set_book_price", methods=["POST"])
def set_book_price():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_id: str = request.json.get("book_id")
    book_price: str = request.json.get("book_price")

    s=seller.Seller()
    code, message=s.set_book_price(user_id,store_id,book_id,book_price)
    return jsonify({"message":message}), code