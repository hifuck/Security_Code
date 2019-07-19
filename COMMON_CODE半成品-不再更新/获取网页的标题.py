# -*- coding:utf-8 -*-
#__author__:langzi
#__blog__:www.langzi.fun

def get_url_title(url):
    try:
        headers = {
            'User-Agent': random.choice(headerss),
            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3'}
        r = requests.get(url=url, headers=headers, verify=False, timeout=10)
        encoding = requests.utils.get_encodings_from_content(r.text)[0]
        res = r.content.decode(encoding, 'replace')
        title_pattern = '<title>(.*?)</title>'
        title = re.search(title_pattern, res, re.S | re.I).group(1)
        return title.replace('\n', '').strip()
    except:
        title = url.split('//')[1].replace('www.', '')
        if '/' in title:
            return title.split('/')[0].replace('\n', '').strip()
        else:
            return title.replace('\n', '').strip()