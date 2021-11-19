import datetime
import urllib
from pymongo import InsertOne, collection, MongoClient
import requests
import re
from lxml import html
from fontTools.ttLib import TTFont
import lxml.html
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
from soupsieve.util import lower

import AutoHomeFont

client = MongoClient('103.85.168.100', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.admin  # 连接对应的数据库名称，系统默认数据库admin

db.authenticate('admin', 'mingtai159888')

collection = db.article_list_qiche
import binascii

def insertdb (data):
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        collection.bulk_write(data)
        print('添加完成'+downloadTime)
    except:
        print('重复添加'+downloadTime)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
# }

# def ziti(rese,content):
#     contents = content.decode('utf-8')
#     rst = re.compile(",url\('(.*?)'\) format\('woff'\);}").findall(str(contents))
#     ttf = requests.get("https:" + rst[0], stream=True)
#     with open("autohome.ttf", "wb") as pdf:
#         for chunk in ttf.iter_content(chunk_size=1024):
#
#             if chunk:
#                 pdf.write(chunk)
#     # 解析字体库font文件
#     font = TTFont('autohome.ttf')
#     bestcmap = font['cmap'].getBestCmap()
#     font.saveXML('autohome1.xml')
#     print(bestcmap)
#     newmap = dict()
#     for key in bestcmap.keys():
#         try:
#             aa = bestcmap[60586]
#             value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
#             key = hex(key)
#             newmap[key] = value
#         except Exception as err:
#             print("異常")
#             import traceback
#             traceback.print_exc()
#             continue
#     print(newmap)
#     content = content.decode('utf-8')
#     for key, value in newmap.items():
#         key_ = key.replace('0x', '&#x') + ';'
#         if key_ in content:
#             response_ = content.replace(key_, str(value))
#
#
#
#     font.saveXML('autohome.xml')
#     uniList  = font['cmap'].tables[0].ttFont.getGlyphOrder()
#
#
#     aaa = uniList[1].encode("utf-8")
#     utf8List = [eval("u'\\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]
#     wordList = ["十", "二", "高", "矮", "长", "大", "近", "四", "更", "远", "右", "了", "着", "下",
#                 "好", "得", "多", "是", "九", "六", "坏", "很", "的", "五", "和", "地", "三", "七",
#                 "小", "左", "一", "呢", "低", "不", "八", "上", "短", "少"]
#     # 获取发帖内容
#     notess = ""
#     note = content
#     for i in range(len(utf8List)):
#         note = note.replace(utf8List[i], wordList[i].encode('utf-8'))
#         print()
#     notess += note.decode('utf-8')
#     return notess
headers = {
    'authority': 'www.autohome.com.cn',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
}
import time
def dizhi():
    res = requests.get('https://club.autohome.com.cn/frontapi/data/page/club_get_topics_list?page_num=2&page_size=50&club_bbs_type=c&club_bbs_id=5395&club_order_type=1')
    content = res.text
    url = re.compile('"pc_url":"http(.*?)",').findall(str(content))
    title = re.compile('"title":"(.*?)",').findall(str(content))
    for til,ur in zip(title,url):
        try:
            print(ur)
            ur = 'https'+ur
            response = requests.get(ur, headers=headers)
            time.sleep(3)
            occ = html.fromstring(response.text)
            oc = response.content.decode('utf-8')
            rst = re.compile(",url\(.*?'(.*?)\'\) format").findall(str(oc))
            ttfurl = "https:"+rst[0]
            ttfurl = ttfurl.replace('\\','')
            ttf = requests.get(ttfurl,headers=headers, stream=True)
            with open("TTF/autohome1.ttf", "wb") as pdf:
                for chunk in ttf.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            standardFontPath = 'TTF/standardFont.ttf'
            newFontPath = 'TTF/autohome1.ttf'
            wordList = AutoHomeFont.get_new_font_dict(standardFontPath, newFontPath)
            font = TTFont('TTF/autohome1.ttf')
            uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
            utf8List = [eval("u'\\u" + uni[3:] + "'") for uni in uniList[1:]]
            # 获取发帖内容
            notess = ""
            note = ""
            occs = occ.cssselect(".post-container ")
            for ocs in occs:
                note += ocs.text_content()
            for i in range(len(utf8List)):
                print()
                note = note.replace(utf8List[i],wordList[i])
            notess += note


            arcontent = re.compile('<div class="post-wrap">([\s\S]*?<div class="post-site">)').findall(str(oc))
            strs = arcontent[0]
            strs = strs.replace('src="//s.autoimg.cn/www/common/images/blank.gif"','')
            strs = strs.replace('data-src','src')
            # articleText = re.compile('<div id="js-vr-top-entry">([\s\S]*?)<div class="post-site">').findall(str(oc))
            list = re.compile('<img.*?src="(.*?)"').findall(str(strs))
            pubtime = re.compile('发表于<strong>(.*?)</strong>').findall(str(oc))
            lists = set(list)
            imgText = ''
            for imgs in lists:
                imgs = "https:"+imgs
                imgText += '<img src="'+imgs+'"></br>'
            articleText = notess+"</br>"+imgText
            site = "汽车之家-昂科旗论坛"
            siteId = 1050203
            pushState = 0
            downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = []
            aid = pubtime[0]+til
            data.append(InsertOne(
                {"url": ur, "title": til, "aid": aid, "content": articleText, "site": site,
                 "pub_time": pubtime[0], "push_state": pushState, "site_id": siteId,
                 "download_Time": downloadTime}))
            insertdb(data)
            huitie = re.compile('<ul class="reply-wrap".*?>([\s\S]*?)</section>').findall(str(oc))
            litext = re.compile('<li[\s\S]*?class="js-reply-floor-container "[\s\S]*?>([\s\S]*?)</li>').findall(str(huitie))
            for iss in litext:
                try:
                    arpubtime = re.compile('发表于<strong>(.*?)</strong>').findall(str(iss))
                    artext = re.compile('<div class="reply-main">([\s\S]*?)<div class="reply-bottom">').findall(str(iss))
                    zhuan = html.fromstring(artext[0])
                    occs = zhuan.cssselect(".reply-detail")
                    notezhu = ''
                    for ocs in occs:
                        notezhu += ocs.text_content()
                    for i in range(len(utf8List)):
                        to = lower(to_unicode(utf8List[i]))
                        notezhu = notezhu.replace(to,wordList[i])
                        notezhu = notezhu.replace('\\n','')
                    data = []
                    aid = arpubtime[0] + til
                    data.append(InsertOne(
                        {"url": ur, "title": til, "aid": aid, "content": notezhu, "site": site,
                         "pub_time": arpubtime[0], "push_state": pushState, "site_id": siteId,
                         "download_Time": downloadTime}))
                    insertdb(data)
                except Exception as err:
                    print("異常")
                    import traceback
                    traceback.print_exc()
                    pass
        except Exception as err:
            print("異常")
            import traceback
            traceback.print_exc()
            pass


def to_unicode(string):
    ret = ''
    for v in string:
        ret = ret + hex(ord(v)).upper().replace('0X', '\\u')

    return ret
if __name__ == "__main__":
    while (True):
        dizhi()
