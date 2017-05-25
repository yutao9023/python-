import requests
from bs4 import BeautifulSoup
import json
import re

# url = 'https://p.3.cn/prices/mgets?callback=jQuery6701655&skuIds=J_10129869293'
# html = requests.get(url).text
# text = re.findall('({.*?})', html)[0]
# print(text)
# JD = json.loads(text)
#
# print(JD['p'])
def parse_index_page(url):
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2141.400 QQBrowser/9.5.10219.400'}
    r = requests.get(url, headers=header)
    r.encoding = r.apparent_encoding
    print(r.text)

def main():
    url = 'https://search.jd.com/Search?keyword=%E5%9B%BE%E4%B9%A6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=3&wq=%E5%9B%BE%E4%B9%A6'
    parse_index_page(url)

main()




















