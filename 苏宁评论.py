import requests
from bs4 import BeautifulSoup
import pymongo
import time
import random

client = pymongo.MongoClient('localhost', 27017)
db = client['suning']
table = db['info']


def get_comment(url):
    hd = {
        'Accept - Encoding': 'gzip, deflate, sdch, br',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Connection': 'keep - alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2141.400 QQBrowser/9.5.10219.400'
    }
    proxy_list = [
        'http://117.177.250.151:8081',
        'http://111.85.219.250:3129',
        'http://122.70.183.138:8118',
        'http://61.232.254.39:3128',
        'http://61.166.151.82:8080',
    ]
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    html = requests.get(url, headers=hd, proxies=proxies).text
    time.sleep(1)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div.rv-target-item > div.rv-target-list')
    for item in items:
        comment = item.select('p.body-content')[0].text.strip()
        comment_time = item.select('div.date.l span')[0].text
        yield {'comment': comment, 'comment_ime': comment_time}


def main(offest):
    url = 'https://review.suning.com/cmmdty_review/general-000000000161358326-0000000000-'+str(offest)+'-total.htm'
    get_comment(url)
    for item in get_comment(url):
        print(item)
        table.insert(item)

if __name__ == '__main__':
    for i in range(1, 51):
        main(i)