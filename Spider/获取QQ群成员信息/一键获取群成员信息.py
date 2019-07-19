# coding:utf-8
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'
# 接口为这个
headers = {
'Host': 'qun.qq.com',
'Connection': 'keep-alive',
'Content-Length': '44',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'https://qun.qq.com',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'https://qun.qq.com/member.html',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
#'Cookie': '修改你自己的COOKIE'
}
data = {
    'gc': '734125103',
    # 群号
    'st': '0',
    # 这个是群成员数值设定，从0开始计数
    'end': '50',
    # 一直到50，意思就是0-50个群成员的信息
    'sort': '0',
    # 这个没研究，不清楚
    'bkn': '11896803'
    # 这个是js的callback唯一对应值
    # 抓包可见

}

r = requests.post(url=url,data=data,headers=headers)
d = eval(r.content)
dd = d['mems']
for x in dd:
    print 'QQ:' + str(x['uin'])
    print 'NAME:' + str(x['nick'])



