import sys 
import os
#把当前文件所在文件夹的父文件夹路径加入到PY

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from be import serve
# from be.model import store
import time
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
# from be.model.init_database import DbSession 
from be.model.init_database import New_order 
from be.model.init_database import New_order_detail 
from be.model.init_database import Store 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # 创建会话




def auto_cancel(): #自动清除订单######CBY
    # conn=store.get_db_conn()
    # cursor=conn.execute("SELECT order_id,time,store_id FROM new_order WHERE order_status = ?", (0,))
    # rows = cursor.fetchall()    #((id,time,store_id ),(id,time,store_id ),...(id,time,store_id ))
    engine = create_engine('postgresql://postgres:mbyc020905@localhost:5432/bookstore')
        # 创建session
    DbSession = sessionmaker(bind=engine)
    session=DbSession()
    rows = session.query(New_order).filter_by(order_status=0).all()

    for content in rows:
        end_time = time.time()
        
        if (end_time - content.time >= 600):  # 付款时间超过10分钟自动取消
            # cursor = conn.execute("UPDATE new_order set order_status = ?"
            #                     "WHERE order_id = ?",(-1, content[0]))   
            session.query(New_order).filter_by(order_id=content.order_id).update({"order_status": -1})
            # cursor_ = conn.execute("SELECT book_id,count FROM new_order_detail WHERE order_id = ?", (content[0],))
            # rows_ = cursor_.fetchall()      #((book_id,cnt),(book_id,cnt),...(book_id,cnt))   
            rows_=session.query(New_order_detail).filter_by(order_id=content.order_id).all()
            for order in rows_:
                # cursor = conn.execute(
                #         "UPDATE store set stock_level = stock_level + ? "
                #         "WHERE store_id = ? and book_id = ? ; ",
                #         (order[1], content[2],order[0]))
                session.query(Store).filter(Store.store_id==content.store_id,Store.book_id==order.book_id).update({Store.stock_level: Store.stock_level + order.count})
    session.commit()

scheduler=BackgroundScheduler() #定义后台执行调度器 
scheduler.add_job(func=auto_cancel, trigger="interval", seconds=5)

if __name__ == "__main__":
    scheduler.start()
    serve.be_run()
