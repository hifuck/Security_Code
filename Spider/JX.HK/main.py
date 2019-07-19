# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()
import smtplib
import re
import time
import datetime
def Get_Content_Of_Url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        r = requests.get(url, headers=headers, verify=False, timeout=5)
        encoding = 'utf-8'
        try:
            encoding = requests.utils.get_encodings_from_content(r.text)[0]
        except:
            pass
        content = r.content.decode(encoding, 'replace')
        return (content, r.status_code)
    except Exception as e:
        return ('langzi', 404)

def Get_Title_Of_Content(content):
    if content[1] != 404:
        Url_Title_pattern = re.compile('<a href="(http.*?)" target="_blank">(.*?)</a>',re.I|re.S)
        res = re.findall(Url_Title_pattern,content[0].strip().replace('\n',''))
        return res[0:-1]

        # for r in res[0:-1]:
        #     print('URL:'+r[0])
        #     print('Title:'+r[1].strip())
# res1 = Get_Content_Of_Url('https://www.xj.hk/?index-2.htm')
#Get_Title_Of_Content(res1[0])

#All_Urls = ['https://www.xj.hk/?index-{}.htm'.format(page) for page in range(1,18)]
Url = 'https://www.xj.hk/?index-1.htm'

Data1 = Get_Title_Of_Content(Get_Content_Of_Url(Url))
if Data1:
    Urls_1 = [x[0] for x in Data1]

# Data_1 = []
# Urls_1 = []

while 1:
    Data_0 = Get_Title_Of_Content(Get_Content_Of_Url(Url))
    if Data_0:
        Urls_0 = [x[0] for x in Data_0]
        Find_Urls = [x for x in Urls_1 if x not in Urls_0]
        print('RunTime : {} , Found {} New Article'.format(datetime.datetime.now(),len(Find_Urls)))
        result = [y for x in Find_Urls for y in Data_0 if x in y[0] ]
        if result != []:
            for ress in result:
                print(ress[0],ress[1].strip())
    time.sleep(3600)
    # Chekc Page 1 hour again
    Data1 = Get_Title_Of_Content(Get_Content_Of_Url(Url))
    if Data1:
        Urls_1 = [x[0] for x in Data1]
