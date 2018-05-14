# coding:utf-8
import requests
import html
res = requests.get("https://www.baidu.com")
body = html.unescape(res.text).replace("<br/>", "\n")
print(body)
