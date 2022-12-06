import sys 
import os
#把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from be import serve
from be.model import store
import time
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler


def auto_cancel(): #自动清除订单######CBY
    conn=store.get_db_conn()
    cursor=conn.execute("SELECT order_id,time,store_id FROM new_order WHERE order_status = ?", (0,))
    rows = cursor.fetchall()    #((id,time,store_id ),(id,time,store_id ),...(id,time,store_id ))
    for content in rows:
        end_time = time.time()
        if (end_time - content[1] >= 600):  # 付款时间超过10分钟自动取消
            cursor = conn.execute("UPDATE new_order set order_status = ?"
                                "WHERE order_id = ?",(-1, content[0]))             
            cursor_ = conn.execute("SELECT book_id,count FROM new_order_detail WHERE order_id = ?", (content[0],))
            rows_ = cursor_.fetchall()      #((book_id,cnt),(book_id,cnt),...(book_id,cnt))          
            for order in rows_:
                cursor = conn.execute(
                        "UPDATE store set stock_level = stock_level + ? "
                        "WHERE store_id = ? and book_id = ? ; ",
                        (order[1], content[2],order[0]))
    conn.commit()

scheduler=BackgroundScheduler() #定义后台执行调度器 
scheduler.add_job(func=auto_cancel, trigger="interval", seconds=5)

if __name__ == "__main__":
    scheduler.start()
    serve.be_run()
