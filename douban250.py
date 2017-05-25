from bs4 import BeautifulSoup
import pymongo
import requests
import re
from requests.exceptions import RequestException

client = pymongo.MongoClient('localhost', 27017)
db = client['douban250']
movie_info = db['movieinfo']


def get_html_text(url):
    try:
        hd = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    movielist = soup.select('.grid_view > li')
    # print(movielist[0])
    for movie in movielist:
        title = movie.select('.title')[0].text
        rank = movie.select('.rating_num')[0].text
        num_of_judge = movie.select('.star span')[3].text
        num_of_judge1 = re.search('(\d+)', num_of_judge).group(0)
        direct = movie.select('.bd p')[0].text.strip()
        actor = '\n主演:'.join(direct.split('   主演:'))
        director = ''.join(actor.split('                           '))
        if movie.select('.inq'):
            comments = movie.select('.inq')[0].text.strip()
        else:
            comments = 'None'
        # movie.append(title, director, comments)
        yield {
            '评分': float(rank),
            '评价人数': int(num_of_judge1),
            '片名': title,
            '导演和主演': director,
            '评论': comments,
        }


def main(offest):
    url = 'https://movie.douban.com/top250?start=' + str(offest) + '&filter='
    html = get_html_text(url)
    for i in parse_one_page(html):
        print(i)
        # movie_info.insert_one(i)


if __name__ == '__main__':
    for i in range(10):
        main(25*i)