# -*- coding: utf-8 -*-
import re
import requests
import html
import time
from bs4 import BeautifulSoup

def crawl_joke_list_use_bs4(page=1):
    url = "http://www.qiushibaike.com/8hr/page/" + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")
    joke_list = soup.find_all("div", class_="article block untagged mb15")
    for child in joke_list:
        print(child.find("h2").string + "\t" + "".join(child.find("div", class_="content").stripped_strings))
    time.sleep(1)

def crawl_joke_list(page=1):
    url = "http://www.qiushibaike.com/8hr/page/" + str(page)
    res = requests.get(url)
    # 获取每个段子div的正则
    pattern = re.compile("<div class=\"article block untagged mb15.*?<div class=\"content\">.*?</div>", re.S)
    # 把 <br/> 替换成换行
    body = html.unescape(res.text).replace("<br/>", "\n")
    m = pattern.findall(body)
    # 抽取用户名的正则
    user_pattern = re.compile("<div class=\"author clearfix\">.*?<h2>(.*?)</h2>", re.S)
    # 抽取段子的正则
    content_pattern = re.compile("<div class=\"content\">(.*?)</div>", re.S)
    for joke in m:
        user = user_pattern.findall(joke)
        output = []
        if len(user) > 0:
            output.append(user[0])
        content = content_pattern.findall(joke)
        if len(content) > 0:
            output.append(content[0].replace("\n", ""))
        print("\t".join(output))
    time.sleep(1)

if __name__ == '__main__':
    crawl_joke_list_use_bs4(1)
    #crawl_joke_list(1)
