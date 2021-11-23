#!/usr/bin/env python
# coding=utf-8
import _thread
import datetime
import re
import threading
import time
import requests
from pymongo import InsertOne, collection, MongoClient

ss = requests.Session()
# client = MongoClient('156.240.119.177', 27017)
client = MongoClient('103.85.168.100', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.admin  # 连接对应的数据库名称，系统默认数据库admin

db.authenticate('admin', 'mingtai159888')

# 连接所用集合，也就是我们通常所说的表
collectiondiaocha = db.article_list_diaochas
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}
def insertdb (data):
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        collectiondiaocha.bulk_write(data)
        print('添加完成'+downloadTime)
    except:
        print('重复添加'+downloadTime)
        # import traceback
        # traceback.print_exc()





def newsuscgmil():
    try:
        response = ss.get('https://www.news.uscg.mil/',headers=headers)
        print(response.status_code)
        content = response.content.decode('utf-8')
        url = re.compile("<a href='https://content.govdelivery.com/(.*?)'").findall(str(content))
        for ur in  url:
            try:
                urls = "https://content.govdelivery.com/"+ur
                print(urls)
                res = ss.get(urls,headers=headers)
                print(res.status_code)
                arcontent = res.content.decode('utf-8')
                title = re.compile('<title>([\s\S]*?)</title>').findall(str(arcontent))
                if title == []:
                    continue
                articleContent = re.compile("<div class='bulletin_body'.*?>([\s\S]*?)</article>").findall(str(arcontent))
                site = "美国海岸警卫队调查处网"
                siteId = 1050072
                data = []
                articleStatue = 0
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(InsertOne(
                    {"url": urls, "title": title[0], "pub_time": downloadTime, "content": articleContent[0],
                     "download_time": downloadTime, "site": site, "site_id": siteId, "aid": urls,
                     'push_state': articleStatue,}))
                insertdb(data)
            except Exception as err:
                import traceback

    except Exception as err:
        import traceback
        print(err)

def navymil():
    try:
        response = ss.get('https://www.navy.mil/Press-Office/Press-Releases/',headers=headers)
        content = response.content.decode('utf-8')
        url = re.compile('<a href="http://www.navy.mil/Press-Office/Press-(.*?)">').findall(str(content))
        for ur in  url:
            try:
                urls = "http://www.navy.mil/Press-Office/Press-"+ur
                res = ss.get(urls,headers=headers)
                arcontent = res.content.decode('utf-8')
                title = re.compile('<title>([\s\S]*?)>').findall(str(arcontent))
                if title == []:
                    continue
                articleContent = re.compile('<div class="divider-container".*?>([\s\S]*?)<div class="aside-container-mobile">').findall(str(arcontent))
                site = "美国海军网"
                siteId = 1050073
                data = []
                articleStatue = 0
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(InsertOne(
                    {"url": urls, "title": title[0], "pub_time": downloadTime, "content": articleContent[0],
                     "download_time": downloadTime, "site": site, "site_id": siteId, "aid": urls,
                     'push_state': articleStatue,}))
                insertdb(data)
            except Exception as err:
                import traceback

    except Exception as err:
        import traceback
        print("1")

def afmil():
    try:
        response = ss.get('https://www.af.mil/News/',headers=headers)
        content = response.content.decode('utf-8')
        url = re.compile('<a href="http://www.af.mil/News/Article-Display(.*?)">').findall(str(content))
        for ur in  url:
            try:
                urls = "http://www.af.mil/News/Article-Display"+ur
                res = ss.get(urls,headers=headers)
                arcontent = res.content.decode('utf-8')
                title = re.compile('<title>([\s\S]*?.)>').findall(str(arcontent))
                if title == []:
                    continue
                articleContent = re.compile('<section class="article-detail-content">([\s\S]*?.)</article>').findall(str(arcontent))
                site = "美国空军"
                siteId = 1050071
                data = []
                articleStatue = 0
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(InsertOne(
                    {"url": urls, "title": title[0], "pub_time": downloadTime, "content": articleContent[0],
                     "download_time": downloadTime, "site": site, "site_id": siteId, "aid": urls,
                     'push_state': articleStatue,}))
                insertdb(data)
            except Exception as err:
                import traceback

    except Exception as err:
        import traceback
        print("1")
def armymil():
    try:
        response = ss.get('https://www.army.mil/news', headers=headers)
        content = response.content.decode('utf-8')
        url = re.compile('<a title=".*?" href="\/article(.*?)">').findall(str(content))
        for ur in  url:
            try:

                urls = "https://www.army.mil/article"+ur
                res = ss.get(urls, headers=headers)
                arcontent = res.content.decode('utf-8')
                title = re.compile('<h1.*?>(.*?)</h1>').findall(str(arcontent))
                if title == []:
                    continue
                articleContent = re.compile('<div class="two-column-body">([\s\S]*?.)<!-- end article-body -->').findall(str(arcontent))
                site = "美国陆军"
                siteId = 1050069
                data = []
                articleStatue = 0
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(InsertOne(
                    {"url": urls, "title": title[0], "pub_time": downloadTime, "content": articleContent[0],
                     "download_time": downloadTime, "site": site, "site_id": siteId, "aid": urls,
                     'push_state': articleStatue,}))
                insertdb(data)
            except Exception as err:
                import traceback

    except Exception as err:
        import traceback
        print("1")
def marinesmil():
    try:
        response = ss.get('https://www.marines.mil/News/',headers=headers)
        content = response.content.decode('utf-8')
        url = re.compile('<a href="http://www.marines.mil/News/(.*?)" >').findall(str(content))
        for ur in  url:
            try:
                urls = "http://www.marines.mil/News/"+ur
                res = ss.get(urls,headers=headers)
                arcontent = res.content.decode('utf-8')
                title = re.compile('<h1.*?>(.*?)</h1>').findall(str(arcontent))
                if title == []:
                    continue
                articleContent = re.compile('<div class="body-text">([\s\S]*?.)<div class="tags-section">').findall(str(arcontent))
                site = "美国海军陆战队总部情报处网"
                siteId = 1050070
                data = []
                articleStatue = 0
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(InsertOne(
                    {"url": urls, "title": title[0], "pub_time": downloadTime, "content": articleContent[0],
                     "download_time": downloadTime, "site": site, "site_id": siteId, "aid": urls,
                     'push_state': articleStatue,}))
                insertdb(data)
            except Exception as err:
                import traceback

    except Exception as err:
        import traceback
        print("1")

def func():
    urll = ['https://www.af.mil/News/','https://www.news.uscg.mil/','https://www.navy.mil/Press-Office/Press-Releases/','https://www.marines.mil/News/','https://www.army.mil/news']

    for ur in urll:
        if 'news.uscg.mil' in ur:
            newsuscgmil()
        if 'navy.mil' in ur:
            navymil()
        if 'af.mil' in ur:
            afmil()
        if 'army.mil' in ur:
            armymil()
        if 'marines.mil' in ur:
            marinesmil()






if __name__ == "__main__":
  a = {'x': 1}
  func()