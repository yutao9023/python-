from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import requests
import os

def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except RequestException:
        return None

def get_chapter_names(html):
    soup = BeautifulSoup(html, 'lxml')
    charpter = soup.select('.bg')
    charpter_names = []
    for entry in charpter[1:]:
        charpter_name = re.findall('<h2>(.*?)</h2>', str(entry))
        file_name = re.findall('<a href.*?>(.*?)</a>', str(entry))
        if charpter_name and file_name:
            for name in file_name:
                name = name.split(' ')[0]
                charpter_names.append(charpter_name[0] + '_' + name)
        else:
            pass
    return set(charpter_names)

def get_each_url(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.select('ul li a')
    for url in urls:
        link = url.get('href')
        text = url.text.split(' ')[0]
        full_name = url.text.replace('?','')
        yield {'url': link, 'text': text,'full_name':full_name}
        print(text)

def get_text(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    items = soup.select('div.content-body')
    item = re.findall(';(.*?);', items[0].text, re.S)
    return item[0].encode()

def save_to_file(url, text, full_name):
    base_dir = 'daomu'
    path = '{}\\{}\\{}'.format(os.getcwd(), base_dir, text)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            pass
    try:
        with open(path +'\\'+ full_name +'.txt', 'wb') as f:
            f.write(get_text(url))
    except:
        pass

def main():
    url = 'http://seputu.com/'
    html = get_html_text(url)
    chapters = get_chapter_names(html)
    for chapter in chapters:
        for each in get_each_url(html):
            if each['text'] == chapter.split('_')[-1]:
                save_to_file(each['url'],chapter,each['full_name'])

if __name__ == '__main__':
    main()
