#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/19 14:51
# @Author : 你就看我秃不秃就完事了
# @Version：V 0.1
# @File : article_dongchedi.py
# @desc :
import requests
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
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
}
client = MongoClient('103.85.168.100', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.admin  # 连接对应的数据库名称，系统默认数据库admin
db.authenticate('admin', 'mingtai159888')
collection = db.article_list_dongche
def dataIns(pubTime,shi):
    if '时' in pubTime:
        tian = 1
    elif '分' in pubTime:
        tian = 1
    elif '秒' in pubTime:
        tian = 1
    elif '天' in pubTime:
        tian = int(shi)
    elif '月' in pubTime:
        tian = int(shi) * 30
    elif '年' in pubTime:
        tian = int(shi) * 365
    threeDayAgo = datetime.datetime.today() - datetime.timedelta(tian)
    pubTimes = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
    return pubTimes


def insertdb (data):
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        collection.bulk_write(data)
        print('添加完成'+downloadTime)
    except:
        print('重复添加'+downloadTime)
response = requests.get('https://www.dongchedi.com/community/4080', headers=headers)
content = response.content.decode('utf-8')
urlList = re.compile('href="/ugc/article/(.*?)"').findall(str(content))
for ur in urlList:
    articleUrl = "https://www.dongchedi.com/ugc/article/"+ur
    articleRequests = requests.get(articleUrl)
    articleContent = articleRequests.content.decode('utf-8')
    mainPost = re.compile('<div class="jsx-\d{5,}">([\s\S]*?.)</div></div></div>').findall(str(articleContent))
    pubTime = re.compile('<p class="jsx-\d{1,}">(.*?)<!-- -->发布<!-- -->于').findall(str(articleContent))
    shi = re.compile('(\d{1,}).*?前').findall(str(pubTime[0]))
    pubTimes = dataIns(pubTime[0],shi[0])

    articleText = re.compile('<div class="jsx-\d{1,} content tw-text-12.*?>([\s\S]*?.)</div></div></div>').findall(str(articleContent))
    #提取文章内容中的汉字 当做标题
    titles = ''
    title = re.compile('([\u4e00-\u9fa5]{1,})').findall(str(articleText))
    for ti in title:
        titles += ti+" "
    print(ur)
    site = "懂车帝"
    siteId = 1050203
    pushState = 0
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = []
    data.append(InsertOne(
        {"url": ur, "title": titles, "aid": ur, "content": articleText[0], "site": site,
         "pub_time": pubTimes, "push_state": pushState, "site_id": siteId,"download_Time": downloadTime}))
    insertdb(data)
    replyContent = re.compile('<ul class="jsx-\d{1,}">([\s\S]*?)<div class="jsx-\d{1,} tw-flex tw-text-12').findall(str(articleContent))
    replyText = re.compile('<li class="jsx-\d{1,} tw-mt-\d">([\s\S]*?.)</li>').findall(str(replyContent))
    replyTexts = re.compile('<span class="jsx-\d{1,}1 jsx-\d{1,} tw-text-common-black">([\s\S]*?)</span>').findall(str(replyContent))
    replyPubTime = re.compile('发表于<!-- -->(\d{1,}).*?前').findall(str(replyContent))
    replyPubTimes = re.compile('发表于<!-- -->(.*?)前').findall(str(replyContent))
    replyPubTimes = dataIns(replyPubTimes[0],replyPubTimes[0])
    replyPubTimess = dataIns(pubTime[0], shi[0])
    for rt,rpt in zip(replyTexts,replyPubTime):
        datas = []
        datas.append(InsertOne(
            {"url": ur, "title": replyTexts[0], "aid": ur, "content": replyTexts[0], "site": site,
             "pub_time": replyPubTimess, "push_state": pushState, "site_id": siteId, "download_Time": downloadTime}))
        insertdb(datas)
    print()
print()