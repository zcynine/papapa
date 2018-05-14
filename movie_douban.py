#!/usr/bin/python
#coding:utf-8
# Filename : get_novel.py

import re
import urllib
import time
import os
import httplib2
import json
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
orgin_url = "https://movie.douban.com/"
def excuSql(sql):
	conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,unix_socket="/data/3306/mysqld.sock",charset='utf8')
	conn.select_db('test')
	cur=conn.cursor()
	result = cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	return result
def checkId(id):
	return excuSql('select * from movie_douban where id_douban = "'+id+'"')
def getHtml(url):
	h2 = httplib2.Http('.cache')
	resp, html = h2.request(url)
	return html
def getMovie(url):
	html = getHtml(url).decode('utf-8')
	reg = ur'https://movie\.douban\.com/subject/(\d*)/.*'
	textre = re.compile(reg)
	textlist = re.findall(textre, html)
	print html
	for texts in textlist:
		recordMovie(texts)
def detailMovie(id):
	movie_url = 'https://movie.douban.com/subject/'+id
	html = getHtml(movie_url)
	html = html.replace('\n','')
	reg = ur'<title>(.*?)</title>';
	titlere = re.compile(reg)
	title = re.search(titlere, html)
	if title is None:
		return title
	title = title.group(1)
	title = title[8:(len(title)-9)]
	reg = ur'<strong class="ll rating_num" property="v:average">(.*?)</strong>.*?<span property="v:votes">(\d*)</span>'
	scorere = re.compile(reg)
	score = re.search(scorere, html)
	if score is None:
		return score
	average = score.group(1)
	numRaters = score.group(2)
	result = {}
	result['title'] = title
	result['rating'] = {}
	result['rating']['average'] =  str(average)
	result['rating']['numRaters'] =  str(numRaters)
	return result
def recordMovie(id):
	if checkId(id) == 1:
		print 'already have'
		return 0
	movie = detailMovie(id)
	if movie is None:
		print 'error'
		return 1
	now_time = str(time.time())
	sql =  'INSERT INTO movie_douban (id_douban, title, score, count_comment, gmt_create, gmt_modified) VALUES ("'+id+'","'+movie['title']+'","'+movie['rating']['average']+'","'+movie['rating']['numRaters']+'","'+now_time+'","'+now_time+'")'
	excuSql(sql)
	print movie['title']+' ' +movie['rating']['average']
	movie_url = 'https://movie.douban.com/subject/'+id
	getMovie(movie_url)
	return 1

print getMovie('https://movie.douban.com/')
