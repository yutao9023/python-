from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db_name = client['phone_number2']
db_table = db_name['info2']


def get_index_urls(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    for item in parse_index_page(url):
        print(item)
        db_table.insert(item)
    if soup.find('a', class_='next'):
        next_url = 'http://nj.58.com' + soup.select('a.next')[0].get('href')
        get_index_urls(next_url)
    else:pass


def parse_index_page(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.boxlist > ul > li')
    for item in info:
        number = item.select('.t strong.number')[0].text
        price = item.select('b.price')[0].text[:-1] if item.find('b', class_='price') else '面议'
        category = item.select('a.t span')[0].text.strip()
        yield {'number': number, 'price': price, 'category': category}


def main():
    url = 'http://nj.58.com/shoujihao/pn1/'
    get_index_urls(url)


main()