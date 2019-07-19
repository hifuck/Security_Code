def scan_baidu(keyword):
    list_001 = []
    print (unicode(' [*] 关键词网址采集功能启动......', 'utf-8'))
    urlx = 'https://www.baidu.com/s?wd='
    for i in range(0, 100, 10):
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        url = str(urlx + str(keyword) + '&pn=' + str(i))
        try:
            r = requests.get(url=url, headers=headers, timeout=timeout)
            rr = re.findall(r'<a target="_blank" href="(.*?)"', r.content, re.S)
            for xx in rr:
                if xx.find('link') > 0:
                    try:
                        rxr = requests.get(url=xx, headers=headers, timeout=5)
                        if rxr.status_code == 200:
                            print (' [*] First Found Url: ' + rxr.url.split('://')[0] + '://' +
                                   rxr.url.split('://')[1].split('/')[0])
                            dxdx = rxr.url.split('://')[0] + '://' + rxr.url.split('://')[1].split('/')[0]
                            if dxdx.find('gov.cn') > 0 or dxdx.find('edu.cn') > 0:
                                pass
                            else:
                                list_001.append(dxdx)
                    except:
                        pass
        except:
            pass