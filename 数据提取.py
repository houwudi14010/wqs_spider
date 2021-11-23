#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/23 18:04
# @Author : 你就看我秃不秃就完事了
# @Version：V 0.1
# @File : 数据提取.py
# @desc :
#----------------------xpth------------------------
import requests
from lxml import etree
def getHTMLtext(url):
    res=requests.get(url,timeout=30)
    # 处理中文编码问题
    res.encoding='gb2312'
    # 转化html
    html=etree.HTML(res.text)
    # xpath提取tr标签下td的内容
    HTMLtext=html.xpath("//tr/td/text()")
    return HTMLtext
#----------------------BeautifulSoup------------------------比较适用于论坛采集
from bs4 import BeautifulSoup
def getHTMLtext(url):
    articleRes = requests.get(url, timeout=30)
    articleContents = articleRes.text
    soup = BeautifulSoup(articleContents,'html.parser')
    soups = soup.select('div[class="l_post l_post_bright j_l_post clearfix"]')
    for pa in soups:
        paa = pa.get_text