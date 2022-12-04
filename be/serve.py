import logging#logging 模块是 Python 内置的标准模块，主要用于输出运行日志，可以设置输出日志的等级、日志保存路径、日志文件回滚等
import os
from flask import Flask
from flask import Blueprint
#Blueprint 是一个存储视图方法的容器，这些操作在这个Blueprint被注册到一个应用之后就可以被调用，Flask可以通过Blueprint来组织URL以及处理请求。
from flask import request
from be.view import auth
from be.view import seller
from be.view import buyer
from be.model.store import init_database


bp_shutdown = Blueprint("shutdown", __name__)

def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@bp_shutdown.route("/shutdown")
def be_shutdown():
    shutdown_server()
    return "Server shutting down..."


def be_run():
    this_path = os.path.dirname(__file__)#得到当前文件的绝对路径(不包括当前文件）..../be
    parent_path = os.path.dirname(this_path)#得到当前文件的绝对路径(不包括当前文件）..../bookstore
    log_file = os.path.join(parent_path, "app.log")
    init_database(parent_path)

    logging.basicConfig(filename=log_file, level=logging.ERROR)
    #使用默认格式化程序创建 StreamHandler 并将其添加到根日志记录器中，从而完成日志系统的基本配置。
    handler = logging.StreamHandler()
    #StreamHandler 类位于核心logging包，它可将日志记录输出发送到数据流例如 sys.stdout, sys.stderr 或任何文件类对象
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )#logging.Formatter函数来配置日志输出内容。
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    app = Flask(__name__)
    app.register_blueprint(bp_shutdown)
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(seller.bp_seller)
    app.register_blueprint(buyer.bp_buyer)

    app.run()
