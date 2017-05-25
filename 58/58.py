from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import re
import time
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)
db = client['58']
url_detail = db['url_detail']
info = db['info']


def get_index_page(url):
    try:
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_index_page(html):
    urllists = []
    soup = BeautifulSoup(html, 'lxml')
    url_list = soup.select('ul.ym-mainmnu  b a')
    for url in url_list:
        url = 'http://nj.58.com' + (url.get('href'))
        urllists.append(url)
    return urllists[:1] + urllists[2:58]


def get_detail_page(url):
    try:
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_detail_page(html):
    soup = BeautifulSoup(html, 'lxml')
    price = soup.select('span.price_now i')
    title = soup.select('h1.info_titile')
    look_time1 = soup.select('span.look_time')
    look_time = re.search('(\d+)', look_time1[0].text).group(0)
    area = soup.select('div.palce_li span i')[0].text if soup.find('div', 'palce_li') else None
    info.insert_one({'price': price[0].text, 'title': title[0].text, 'look_time': look_time, 'area': area})
    print({'price': price[0].text, 'title': title[0].text, 'look_time': look_time, 'area': area})


def get_final_html(url):
    try:
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def get_all_detail_urls(url, page_num):
    hd = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
    url_view = "{}/0/pn{}".format(url, str(page_num))
    html = requests.get(url_view, headers=hd).text
    time.sleep(0.3)
    soup = BeautifulSoup(html, 'lxml')
    if not soup.find('div.noinfotishi'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href')
            if 'detail' in item_link:
                # url_detail.insert_one({'url_detail': item_link})
                # print(item_link)
                yield item_link
            else:
                pass
    else:
        pass


def main():
    url = 'http://nj.58.com/sale.shtml'
    html = get_index_page(url)
    for link in parse_index_page(html):
        for i in range(1, 101):
            for item_link in get_all_detail_urls(link, i):
                web_data = get_final_html(item_link)
                parse_detail_page(web_data)

if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main,)
    main()

