# -*- coding:utf-8 -*-


#__author__:langzi
#__blog__:www.langzi.fun
import pymysql
sqls = [x.strip() for x in open('sql.txt','r',encoding='utf-8').readlines()]
coon = pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='lang_cms_find',port=3306)
cursor = coon.cursor()
for i in sqls:
    try:
        cursor.execute(i)
        print('success')
    except Exception as e:
        print('faild')
    finally:
        coon.commit()
cursor.close()
coon.close()
#
# urls = [x.strip() for x in open('result.txt','r',encoding='utf-8').readlines()]
# with open('sql.txt','a+')as a:
#     for i in urls:
#         a.write(f'insert into url_index(url) values ("{i}");\n')