import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup
from hashlib import md5
from multiprocessing import Pool

def get_html_text(url):
    try:
        hd = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return ''


def parse_one_page_(html):
    lis = []
    soup = BeautifulSoup(html, 'html.parser')
    urllist = soup.select('#index-flex-images img')
    for url in urllist:
        pic = re.findall('data-original="(.*?)"', str(url))
        lis.append(pic[0])
    return lis


def write_to_file(url_list):
    for url in url_list:
        pic = requests.get(url)
        with open('pic3\\'+str(md5(pic.content).hexdigest())+'.jpg', 'wb') as f:
            print('正在下载图片{}'.format(md5(pic.content)))
            f.write(pic.content)

        # f = open('pic2\\'+str(count)+'.jpg', 'wb')
        # print('正在下载图片{}'.format(count))
        # f.write(pic3.content)
        # count += 1


def main(offeset):
    url = 'http://588ku.com/beijing/0-31-pxnum-0-8-0-0-0-' + str(offeset)
    html = get_html_text(url)
    write_to_file(parse_one_page_(html))


if __name__ == '__main__':
    # for i in range(1, 10):
    #     main(i)
    pool = Pool()
    pool.map(main, [i for i in range(1, 10)])
