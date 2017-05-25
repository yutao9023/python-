import pymongo
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import re

client = pymongo.MongoClient('localhost', 27017)
db = client['maoyan']
table = db['movieinfo']


def get_html_text(url):
    try:
        hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    movieList = soup.select('dd')
    for movie in movieList:
        img_src = re.findall('data-src="(.*?)"/>', str(movie))
        name = re.findall('title="(.*?)">', str(movie))
        pb_time = re.findall('releasetime">(.*?)</p>', str(movie))
        actor = re.findall('star">(.*?)</p>', str(movie), re.S)
        print(actor[0].strip()[3:])
        print(img_src[0])
        yield {
            '图片地址': img_src[0],
            '电影名': name[0],
            '上映时间': pb_time[0],
            '主演': actor[0].strip()[3:]

        }


def save_to_mongo(item):
    if table.insert(item):
        print('插入mongodb成功')
    else: print('失败')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_html_text(url)
    parse_one_page(html)
    movie = parse_one_page(html)
    for item in movie:
        save_to_mongo(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)