from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import time

# def get_page_html(url):
#     try:
#         hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
#
#         r = requests.get(url, headers=hd)
#         r.raise_for_status()
#         r.encoding = r.apparent_encoding
#         return r.text
#     except RequestException:
#         return None


def get_all_detail_urls(url, page_num):
    hd = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'}
    url_view = "{}/0/pn{}".format(url, str(page_num))
    html = requests.get(url_view, headers=hd).text
    time.sleep(0.5)
    soup = BeautifulSoup(html, 'lxml')
    if not soup.find('div.noinfotishi'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href')
            if 'detail' in item_link:
                print(item_link)
            else:pass
    else:
        pass


def main():
    url = 'http://nj.58.com/diannaopeijian/'
    # html = get_page_html(url)
    for i in range(1, 101):
        get_all_detail_urls(url, i)

if __name__ == '__main__':
    main()