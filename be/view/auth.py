from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import user


bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login", methods=["POST"])
def login():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    terminal = request.json.get("terminal", "")
    u = user.User()
    code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    u = user.User()
    code, message = u.logout(user_id=user_id, token=token)
    return jsonify({"message": message}), code


@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = user.User()
    code, message = u.register(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = user.User()
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/password", methods=["POST"])
def change_password():
    user_id = request.json.get("user_id", "")
    old_password = request.json.get("oldPassword", "")
    new_password = request.json.get("newPassword", "")
    u = user.User()
    code, message = u.change_password(user_id=user_id, old_password=old_password, new_password=new_password)
    return jsonify({"message": message}), code

###lsq:精确搜索书名
@bp_auth.route("/search_title", methods=["POST"])
def search_title():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_title(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:精确搜索作者名
@bp_auth.route("/search_author", methods=["POST"])
def search_author():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_author(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索title
@bp_auth.route("/search_title_inexact", methods=["POST"])
def search_title_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_title_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索author
@bp_auth.route("/search_author_inexact", methods=["POST"])
def search_author_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_author_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索tag
@bp_auth.route("/search_tag_inexact", methods=["POST"])
def search_tag_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_tag_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索content
@bp_auth.route("/search_content_inexact", methods=["POST"])
def search_content_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_content_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code
    