#coding:cp936
import sys
import re
reload(sys)
sys.setdefaultencoding('cp936')

sql_result = {}
import subprocess
comm = "sqlmap.py -u http://127.0.0.1/sqli/Less-1/?id=1 --batch --technique=B"
try:
    res = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
    result = res.stdout.read()
    print result
    print '-'*50
    result = result.replace('\n','')
    print result
    if 'Parameter' in result:
        print '666'
        if result.count('Type')>1:
            pattern = 'Parameter: (.*?)    Type: (.*?)    Title: (.*?)    Payload: (.*?)    .*DBMS is (.*?)web server operating system: (.*?)web application technology: (.*?)back-end DBMS: (.*?)\['
            #pattern = 'Parameter: (.*?)    Type: (.*?)    Title: (.*?)    Payload: (.*?)---\[.*DBMS is (.*?)web server operating system: (.*?)web application technology: (.*?)back-end DBMS: (.*?)\['
            r = re.findall(pattern,result,re.S)
            for parameter,type,title,Payload,db,system,application,dbms in r:
                sql_result['parameter'] = parameter
                sql_result['type'] = type
                sql_result['title'] = title
                sql_result['Payload'] = Payload
                sql_result['db'] = db
                sql_result['system'] = system
                sql_result['application'] = application
                sql_result['dbms'] = dbms

            print sql_result
        else:
            pattern = 'Parameter:(.*?)Type:(.*?)Title:(.*?)Payload:(.*?)\[.*?endDBMSis(.*?)webserveroperatingsystem:(.*?)webapplicationtechnology:(.*?)back-endDBMS:(.*?)\['
            pattern = 'Parameter: (.*?)    Type: (.*?)    Title: (.*?)    Payload: (.*?)---\[.*DBMS is (.*?)web server operating system: (.*?)web application technology: (.*?)back-end DBMS: (.*?)\['

            r = re.findall(pattern,result,re.S)
            for parameter, type, title, Payload, db, system, application, dbms in r:
                sql_result['parameter'] = parameter
                sql_result['type'] = type
                sql_result['title'] = title
                sql_result['Payload'] = Payload
                sql_result['db'] = db
                sql_result['system'] = system
                sql_result['application'] = application
                sql_result['dbms'] = dbms

            print sql_result

except Exception,e:
    print e

print '*'*50
print res.poll()