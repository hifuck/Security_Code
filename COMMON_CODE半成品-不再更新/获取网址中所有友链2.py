import re
import random
import requests
import time
headerss = [
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)',
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)',
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)',
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
]

def get_urls(url):
    urlss = []
    live_urls = []
    UA = random.choice(headerss)
    headers = {'User-Agent': UA}
    try:
        r = requests.get(url=url, headers=headers, verify=False, timeout=5)
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)
        urls = re.findall(pattern, r.content.decode())

        for x in urls:
            a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
            a3 = ''.join(a1) + '//' + ''.join(a2)
            urlss.append(a3.replace("'", "").replace('>', '').replace('<', ''))
        print(urlss)
        time.sleep(500)
        if urlss:
            for _ in list(set(urlss)):
                UA = random.choice(headerss)
                headers = {'User-Agent': UA}
                try:
                    rr = requests.head(url=_, headers=headers, timeout=5, verify=False)
                    if rr.status_code == 200:
                        live_urls.append(_)
                    else:
                        pass
                except:
                    pass
            return live_urls
        else:
            return None
    except Exception as e:
        print(e)

print(get_urls('http://www.hntky.com'))