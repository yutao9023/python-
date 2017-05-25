from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db_name = client['rent']
db_talbe = db_name['info']


def get_index_page(url):
    try:
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        return r.text
    except RequestException:
        return None


def parse_index_page(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('.resule_img_a')
    for url in links:
        yield url.get('href')


def get_detail_page(url):
    try:
        hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_detail_page(html):
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('span', class_='zm_ico'):
        title = soup.select('div.pho_info h4 em')[0].text
        area = soup.select('p span.pr5')[0].text.strip()
        price = soup.select('div.day_l span')[0].text
        house_url = soup.select('#curBigImage')[0].get('src')
        lorder_name = soup.select('a.lorder_name')[0].text
        lorder_url = soup.select('div.member_pic a img')[0].get('src')
        credit = soup.select('span.zm_ico')[0].text
        gender = 'boy' if soup.find('span', class_='member_boy_ico') else 'girl'
        db_talbe.insert_one({'price': price, 'title': title, 'area': area, 'house_url': house_url,
                             'lorder_name': lorder_name, 'lorder_url': lorder_url, 'credit': credit, 'gender': gender})
        print({'price': price, 'title': title, 'area': area, 'house_url': house_url,
                             'lorder_name': lorder_name, 'lorder_url': lorder_url, 'credit': credit, 'gender': gender})
    else:print('没芝麻信用分')


def main(offest):
    url = 'http://nj.xiaozhu.com/search-duanzufang-p'+str(offest)+'-0/'
    html = get_index_page(url)
    for link in parse_index_page(html):
        web_data = get_detail_page(link)
        parse_detail_page(web_data)

if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i for i in range(1, 14)])
    for i in range(1, 14):
        main(i)
    # for i in db_talbe.find():
    #     if i['price'] >= 500:
    #         print(i)