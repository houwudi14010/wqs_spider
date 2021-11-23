#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/22 11:54
# @Author : 你就看我秃不秃就完事了
# @Version：V 0.1
# @File : twitter_user.py
# @desc :
import datetime
import re
import threading
import time
import requests
from bson import ObjectId
from pymongo import InsertOne, collection, MongoClient
# 导入pymysql模块
import pymysql
# 连接database
conn = pymysql.connect(host='localhost', user='root',password='123456',database='article',charset='utf8')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
ss = requests.Session()
# client = MongoClient('156.240.119.177', 27017)
client = MongoClient('103.85.168.100', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.admin  # 连接对应的数据库名称，系统默认数据库admin
db.authenticate('admin', 'mingtai159888')
collectionpengyouquan = db.article_list_tuiteAuthor
collection = db.article_list_tuiteAuthors
lists = ''
quchong_list = ''
for i in range(1,5):
    datas = (list(collectionpengyouquan.find({}, {"authorStatue": 0,})))
    # 定义要执行的SQL语句
    sql = "INSERT INTO g_yq_source_twitter(twitter_id,twitter_name,twitter_account) VALUES (%s,%s,%s);"
    for data in datas:
        a = data['auName']
        key_list = list(a.split('&~~&'))
        a = key_list[0]+"櫷"+key_list[1]+"櫷"+key_list[1]+"\n"
        if key_list[1] in quchong_list:
            continue
        else:
            lists += a
            quchong_list += key_list[1]+" "

    downloadTime = datetime.datetime.now().strftime('%H%M%S')
    with open("test.txt", "a",encoding='utf-8' ) as f:
        f.write(str(lists))

    # 执行SQL语句
    # cursor.execute(sql, [twitter_id, twitter_name, twitter_account])
    # conn.commit()
# # 关闭光标对象
# cursor.close()
# # 关闭数据库连接
# conn.close()



# for key in datas:
#     auName = key['auName']
#     key_list = list(auName.split('&~~&'))
#     data = []
#     data.append(InsertOne(
#         {"twitter_name":key_list[0],"twitter_account":key_list[1]}))
#     try:
#         collection.bulk_write(data)
#         print('添加完成')
#     except:
#         print('重复添加')
#     collectionpengyouquan.update_one({"auName": auName}, {'$set': {"authorStatue": 1}})
# client.close()
# print()




