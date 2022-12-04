import sys 
import os
#把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from be import serve
from be.model import store
import time

def auto_cancel(): #自动清除订单######CBY
    conn=store.get_db_conn()
    cursor=conn.execute("SELECT order_id,time FROM new_order WHERE order_status = ?", (0,))
    rows = cursor.fetchall()    #((id,time,),(id,time,),...(id,time,))

    for content in rows:
        end_time = time.time()
        if (end_time - content[1] >= 600):  # 付款时间超过10分钟自动取消
            cursor = conn.execute("UPDATE new_order set order_status = ?"
                                "WHERE order_id = ?",(-1, content[0])) 
    conn.commit()


if __name__ == "__main__":
    serve.be_run()
