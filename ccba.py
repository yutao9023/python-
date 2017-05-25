from bs4 import BeautifulSoup
import requests
import pymongo
import re

def parse_index_page(url):
    html = requests.get(url).text
    urls = re.findall('src="(.*?.gif)"', html)
    return urls

def main():
    count = 1
    for i in range(1,12):
        url = 'http://ccba.me/71292-'+str(i)+'.html'
        for link in parse_index_page(url):
            pic = requests.get(link)
            with open('pic3\\' + str(count) + '.gif', 'wb') as f:
                print('\r正在下载第{}张图片'.format(count))
                count += 1
                f.write(pic.content)


if __name__ == '__main__':
    main()


