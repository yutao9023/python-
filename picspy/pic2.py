import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_html_text(url):
    try:
        hd = {
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': 'thw=us; miid=155873786877091278; tracknick=tb_0577569; _cc_=URm48syIZQ%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; t=e32bb5cc93bef1f876c878bc13841231; _tb_token_=ggswVmmp0BTk; cookie2=d91d7ab3d9052addf4d5f9723fb8722c; v=0; linezing_session=TgJv8FPmMTA7scQMS616UT42_14933852011808Lzv_1; mt=ci%3D-1_0; cna=4N9fEHFPQ0ACAdoC2BWYV0mZ; _m_h5_tk=f9ef04fcb0ef54d14a47bb0bdc67e546_1493394136501; _m_h5_tk_enc=cb124aa1dbaa2a676b539766a35af941; l=Avf3mW0duCA1uGRQ1Kba9UXcB/BBvMse; isg=AoWF8W7-cAerUlqrQ70xX1G-lMG-JHWxWOTwWofqQbzLHqWQT5JJpBP4WvgX',
            'Referer': 'https://m.taobao.com/?sprefer=sypc00&spm=a230r.1.0.0.Nomp8v&_t_t_t=0.44067462617799835',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return ''


def parse_one_page_(html, lis):
    soup = BeautifulSoup(html, 'html.parser')
    urllist = soup.select('#index-flex-images img')
    for url in urllist:
        pic = re.findall('data-original="(.*?)"', str(url))
        lis.append(pic[0])
    # return lis


def write_to_file(url_list):
    count, c = 0, 0
    for url in url_list:
        pic = requests.get(url)
        with open('pic2\\'+str(c)+'.jpg', 'wb') as f:
            print('\r正在下载第{}张图片'.format(count))
            count += 1
            f.write(pic.content)
            print("\r当前进度: {:.2f}%".format(count * 100 / len(url_list)), end="")
        c += 1


def main():
    url_list = []
    for i in range(1, 20):
        url = 'http://588ku.com/beijing/0-31-pxnum-0-8-0-0-0-' + str(i)
        html = get_html_text(url)
        parse_one_page_(html, url_list)
    write_to_file(url_list)

if __name__ == '__main__':
    pool = Pool()
    # pool(main)
    main()