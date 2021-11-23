import datetime
import threading
import subprocess

import requests
from json_extract import GetValue2
from pymongo import InsertOne, collection, MongoClient
from selenium import webdriver  # 驱动浏览器
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕 寻找某些元素
import time
import datetime
import re
import threading
import time
import traceback
import requests
from bs4 import BeautifulSoup
from pymongo import InsertOne, collection, MongoClient
# import test
# class Login(test.test):
#     pass
# if __name__ == '__main__':
#     Login()

aa = []
for i in range(1,1001):
    for b in range(1,i):
        if i % b == 0:
            aa.append(b)
    if sum(aa) == i:
        print("{}是完数 因子包括{}".format(i,aa))
    aa.clear()

