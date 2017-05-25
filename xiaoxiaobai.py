import requests
import re
import random
from hashlib import md5
from multiprocessing import Pool
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['tumblr']
table = db['xiaoxiaobai']

def get_html_text(url):
    s = requests.Session()
    header = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
     }
    proxy_list = [
        'http://117.177.250.151:8081',
        'http://111.85.219.250:3129',
        'http://122.70.183.138:8118',
    ]
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxies = {'http': proxy_ip}
    r = s.get(url, headers=header, proxies=proxies, verify=False)
    return r

def parse_index_page(html):
    urllist  = []
    urls = re.findall('img src="(.*?)" alt',  html.text)
    for url in urls:
        urllist.append(url)
    return urllist


def save_to_file(urllist):
    for url in urllist:
        table.insert_one({'url': url})
        pic = get_html_text(url)
        with open('pic\\' + str(md5(pic.content).hexdigest()) + '.gif', 'wb') as f:
            f.write(pic.content)
            print('正在下载：' + str(url))

def main(offest):
    url = 'https://xiaoxiaobai12138.tumblr.com/page/' + str(offest)
    html = get_html_text(url)
    urllist = parse_index_page(html)
    save_to_file(urllist)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(10, 68)])
# for i in range(1,10):
#     main(i)
