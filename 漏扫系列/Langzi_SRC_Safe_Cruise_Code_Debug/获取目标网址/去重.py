import re
all_ips=list(set([x.strip().replace(',','\n') for x in open('ip.txt','r',encoding='utf-8').readlines()]))
# for x in all_ips:
#     print(x)

with open('ip_res.txt','a+',encoding='utf-8')as a:
    for x in all_ips:
        a.write(x+'\n')