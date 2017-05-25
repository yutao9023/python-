# __author__ = 'Taoyu'
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['goods_info']
mongo_table = db['goods_info']


def get_html_text(url):
    try:
        hd = {
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Content-type':'application/x-www-form-urlencoded',
            'Cookie':'thw=us; miid=155873786877091278; tracknick=tb_0577569; _cc_=URm48syIZQ%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; t=e32bb5cc93bef1f876c878bc13841231; _tb_token_=ggswVmmp0BTk; cookie2=d91d7ab3d9052addf4d5f9723fb8722c; v=0; linezing_session=TgJv8FPmMTA7scQMS616UT42_14933852011808Lzv_1; mt=ci%3D-1_0; cna=4N9fEHFPQ0ACAdoC2BWYV0mZ; _m_h5_tk=f9ef04fcb0ef54d14a47bb0bdc67e546_1493394136501; _m_h5_tk_enc=cb124aa1dbaa2a676b539766a35af941; l=Avf3mW0duCA1uGRQ1Kba9UXcB/BBvMse; isg=AoWF8W7-cAerUlqrQ70xX1G-lMG-JHWxWOTwWofqQbzLHqWQT5JJpBP4WvgX',
            'Referer':'https://m.taobao.com/?sprefer=sypc00&spm=a230r.1.0.0.Nomp8v&_t_t_t=0.44067462617799835',
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('"raw_title":"(.*?)".*?"view_price":"(.*?)".*?"item_loc":"(.*?)".*?"view_sales":"(.*?)人付款"'
                         '.*?"nick":"(.*?)".*?"shopcard"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        print(item)
        yield {
            '商品名': item[0],
            '价格': float(item[1]),
            '发货地': item[2],
            '付款人数': int(item[3]),
            '商店名': item[4]
        }


def write_to_file(content):
    with open('goods.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offest):
    url = 'https://s.taobao.com/search?q=%E8%83%8C%E5%8C%85&bcoffset=1&ntoffset=1&p4ppushleft=1%2C48&s=' + str(offest)
    html = get_html_text(url)
    item = parse_one_page(html)
    for i in item:
        # write_to_file(i)
        mongo_table.insert(i)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*44 for i in range(10)])
    # for i in range(100):
    #     main(i*44)
