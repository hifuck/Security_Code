import requests
import re
import pymysql
import time
import configparser
import contextlib
from bs4 import BeautifulSoup as bs
import random
requests.packages.urllib3.disable_warnings()
timeout = 5

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
first_cule = ['.com.cn', '.org.cn', '.net.cn', '.com', '.cn', '.cc', '.net', '.org', '.info', '.fun', '.one', '.xyz',
              '.name', '.io', '.top', '.me', '.club', '.tv']


def get_url_from_content(url):
    '''

    根据传入网址
    获取该网址页面中的友链，满足下面2条件：
        1. 域名中带有www.
        2. 必须访问成功
    :param url:
    :return:
    '''
    result_list = []
    result_set = []
    mid_result = []
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA, 'Connection': 'close'}
        r = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        time.sleep(0.02)
        bp = bs(r.content, 'html.parser')
        for x in bp.select('li > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    print(e)
            else:
                pass
        for x in bp.select('td > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    print(e)
            else:
                pass
        for x in bp.select('p > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    print(e)
            else:
                pass
        for x in bp.select('div > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    print(e)
            else:
                pass
    except Exception as e:
        print(e)

    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA, 'Connection': 'close'}
        r = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        time.sleep(0.02)
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)
        encoding = requests.utils.get_encodings_from_content(r.text)[0]
        res = r.content.decode(encoding, 'replace')
        urls = re.findall(pattern, res)
        for x in urls:
            a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
            a3 = ''.join(a1) + '//' + ''.join(a2)
            result_list.append(a3.replace("'", "").replace('>', '').replace('<', ''))
    except:
        pass

    result_list = list(set(result_list))
    print(result_list)
    print(len(result_list))

    for u in result_list:
        if 'www.' in u:
            mid_result.append(u)

    for u in mid_result:
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA, 'Connection': 'close'}
            r = requests.get(url=u, headers=headers, verify=False, timeout=timeout)
            time.sleep(0.02)
            if r.status_code == 200:
                result_set.append(u)
        except:
            pass
    print(len(result_set))
    return result_set

print(get_url_from_content('http://www.hntky.com/'))
