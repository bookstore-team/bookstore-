from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import user

bp_search = Blueprint("search", __name__, url_prefix="/search")


@bp_search.route("/param_search", methods=["POST"])
def param_search():
    title = request.json.get("title", "")
    author = request.json.get("author", "")
    tag = request.json.get("tag", "")
    store_id = request.json.get("store_id", "")
    u = user.User()
    code, message = u.params_search(title=title, author=author, tag=tag,  store_id=store_id)
    # code, message = u.params_search(title=title, author=author, tag=tag)
    return jsonify({"message": message}), code


@bp_search.route("/content_search", methods=["POST"])
def content_search():
    content: str = request.json.get("content")
    store_id = request.headers.get("store_id")
    u = user.User()
    code, message = u.whole_content_search(content=content, store_id=store_id)
    return jsonify({"message": message}), code