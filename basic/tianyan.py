# coding:utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib

driver = webdriver.PhantomJS(executable_path='/Users/zcynine/.nvm/versions/node/v8.3.0/bin/phantomjs')

def search(keyword):
    url_keyword = urllib.parse.quote(keyword)
    url = "http://www.tianyancha.com/search/" + url_keyword + "?checkFrom=searchBox"
    print(url)
    driver.get(url)
    bsObj = BeautifulSoup(driver.page_source, "html5lib")
    print(bsObj)
    company_list = bsObj.find_all("span", attrs={"ng-bind-html": "node.name | trustHtml"})
    for company in company_list:
        print(company.get_text())

if __name__ == '__main__':
    search("阿里巴巴 马云")
