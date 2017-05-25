from bs4 import BeautifulSoup
import requests
import re
import os

hd = {
    'Accept':'image/png, image/svg+xml, image/jxr, image/*;q=0.8, */*;q=0.5',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
    'Pragma': 'no-cache',
}


def get_html_text(url):
    r = requests.get(url, headers=hd)
    return r.text


def get_index_urls(url):
    html = get_html_text(url)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('tbody > tr')
    for item in items:
        url = item.select('td.tit a')[0].get('href')
        link = 'http://www.kuaikanmanhua.com/' + url
        title = item.select('td.tit a')[0].get('title')
        data = re.findall('<td>(.*?)</td>', str(item))
        yield {'link': link,'title':title,'data':data[0]}


def pare_index_page(url):
    html = get_html_text(url)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div.list.comic-imgs > img')
    for item in items:
        src = re.findall('data-kksrc="(.*?)" h', str(item), re.S)
        yield src[0].replace('amp;', '')


def save_to_file(index_url, urllist):
    count = 1
    base_dir = 'commic'
    path = '{}\\{}\\{}\\'.format(os.getcwd(), base_dir, index_url['title'])
    if not os.path.exists(path):
        os.makedirs(path)
    for url in urllist:
        pic = requests.get(url, headers=hd)
        with open(path + str(count) + '.jpg', 'wb') as f:
            f.write(pic.content)
            print('正在保存 {}这张图片到 {}中'.format(url, path))
            count += 1


def main():
    urllist = []
    url = 'http://www.kuaikanmanhua.com/web/topic/178/'
    for index_url in get_index_urls(url):
        for img_src in pare_index_page(index_url['link']):
            urllist.append(img_src)
        save_to_file(index_url, urllist)
        print('又是一话啦')
        urllist = []
    print('下载完成咯')
if __name__ == '__main__':
    main()