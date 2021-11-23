#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/19 14:51
# @Author : 你就看我秃不秃就完事了
# @Version：V 0.1
# @File : article_dongchedi.py
# @desc :
import datetime
from pymongo import InsertOne, collection, MongoClient
import requests
import re
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
}
client = MongoClient('103.85.168.100', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.admin  # 连接对应的数据库名称，系统默认数据库admin
db.authenticate('admin', 'mingtai159888')
collection = db.article_list_dongche
def dataInss(pubTime):
    tians = 99
    if '时' in pubTime:
        tians = 0
    elif '分' in pubTime:
        tians = 0
    elif '秒' in pubTime:
        tians = 0
    elif '前天' in pubTime:
        tians = 2
    elif '昨天' in pubTime:
        tians = 1
    elif '月' in pubTime:
        tians = 30
    elif '年' in pubTime:
        tians = 365
    elif '刚刚' in pubTime:
        tians = 0
    elif '天前' in pubTime:
        aums = re.compile('(.*?)天前').findall(str(pubTime))
        tians = int(aums[0])
    else:
        downloadTime = datetime.datetime.now().strftime('%Y')
        pubTime = str(downloadTime)+'-'+pubTime+" 00:00:00"
    if tians == 99:
        return pubTime
    else:
        threeDayAgo = datetime.datetime.today() - datetime.timedelta(tians)
        pubTimes = threeDayAgo.strftime("%Y-%m-%d")
        pubTimes = pubTimes+" 00:00:00"
    return pubTimes

def insertdb (data):
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        collection.bulk_write(data)
        print('添加完成'+downloadTime)
    except:
        print('重复添加'+downloadTime)

def func():
    response = requests.get('https://www.dongchedi.com/community/4080', headers=headers)
    content = response.content.decode('utf-8')
    urlList = re.compile('href="/ugc/article/(.*?)"').findall(str(content))
    for ur in urlList:
        try:
            articleUrl = "https://www.dongchedi.com/ugc/article/"+ur
            articleRequests = requests.get(articleUrl)
            articleContent = articleRequests.content.decode('utf-8')
            pubTime = re.compile('<p class="jsx-\d{1,}">(.*?)<!-- -->发布<!-- -->于').findall(str(articleContent))
            authorName = re.compile('"name":"(.*?)","media_id').findall(str(articleContent))
            pubTimes = dataInss(pubTime[0])
            articleText = re.compile('<div class="jsx-\d{1,} content tw-text-12.*?>([\s\S]*?.)</div></div></div>').findall(str(articleContent))
            titles = re.compile('<title>(.*?)</title>').findall(str(articleContent))
            site = "懂车帝"
            siteId = 1050203
            pushState = 0
            downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = []
            data.append(InsertOne(
                {"url": articleUrl, "title": titles[0], "aid": ur, "content": articleText[0], "site": site,"author":authorName[0],
                 "pub_time": pubTimes, "push_state": pushState, "site_id": siteId,"download_Time": downloadTime}))
            insertdb(data)
        except Exception as err:
            import traceback
            traceback.print_exc()
            pass
        try:
            replyContent = re.compile('<ul class="jsx-\d{1,}">([\s\S]*?)<div class="jsx-\d{1,} tw-flex tw-text-12').findall(str(articleContent))
            replyTexts = re.compile('<span class="jsx-\d{1,}1 jsx-\d{1,} tw-text-common-black">([\s\S]*?)</span>').findall(str(replyContent))
            replyPubTime = re.compile('发表于<!-- -->(.*?)</span>').findall(str(replyContent))
            author = re.compile('title="(.*?)个人主页 "').findall(str(replyContent))
            for rt, rpt,au in zip(replyTexts,replyPubTime,author):
                try:
                    replyPubTimes = dataInss(rpt)
                    datas = []
                    datas.append(InsertOne(
                        {"url": articleUrl, "title": titles[0], "aid": rt, "content": rt, "site": site,"author":au,
                         "pub_time": replyPubTimes, "push_state": pushState, "site_id": siteId, "download_Time": downloadTime}))
                    insertdb(datas)
                except Exception as err:
                    import traceback
                    traceback.print_exc()
                    pass
        except Exception as err:
            import traceback
            traceback.print_exc()
            pass
if __name__ == "__main__":
    while (True):
        func()
