#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/19 16:35
# @Author : 你就看我秃不秃就完事了
# @Version：V 0.1
# @File : 汽车之家视频.py
# @desc :
# coding=utf-8

import requests

"""
汽车之家视频爬取
"""

url = "https://n26-pl-agv.autohome.com.cn/video-45/E3BD4E39114FD258/2020-04-21/6146950A3CCB2DE86F15C4841F4F2CE2-300.mp4?key=4EBD47E7109AC1E0F1EC0273C7780639&time=1588134095"

# url = "https://vdhkto3.bdstatic.com/625647493343793750586764534d714c/4c446e6d7a794a43/03afedb26faaf1e41be403a18b43f420150c10dcc6a5d41597cbdefe44be07118ee463dda98ebd3fee7b9c38d5e4a02dbc646443ec5e1990e11c215dbcbaf804.mp4?auth_key=5ea8f782-0-0-debbf4c4791c9a44c6ed5426e0689bb1&bcevod_channel=third_party_partners&pd=52&vt=1&cd=0&did=&logid=2280687185&vid=11293573895490280932&pt=0&cr=2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}

response = requests.get(url=url, headers=headers)

with open('xiaopin.mp4', 'wb+') as f:
    f.write(response.content)
