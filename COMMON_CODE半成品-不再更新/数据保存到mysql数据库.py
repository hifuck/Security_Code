import contextlib
@contextlib.contextmanager
def co_mysql(db='mysql'):
    conn = pymysql.connect(host=HOST,user=USER,password=PASSWORD,port=PORT,db=db,charset='utf8')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# 自动创建数据库

'''

判断数据库中是否存在该数据库

'''
with co_mysql(db='mysql') as cursor:
   row_count = cursor.execute("show databases;")
   a = cursor.fetchall()
   b = [y for x in a for y in x]
   if DATABASE in b:
       pass
   else:
       cursor.execute("create database "+ DATABASE )
