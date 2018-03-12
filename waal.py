#!/usr/bin/env python  
#-*- coding: utf-8 -*-
from lxml import etree
import requests
import csv
import requests
import json
import jsonpath  
import time
import codecs
import HTMLParser
import re
import js2xml

e_headers = ['名字','会员级别','评论内容','评论时间','点赞数','评论数','评价星级']

headers = {
	'Cookie':'',
	'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
}

#获取手机URL
def get_phone_url(html_comtent):
	list_phone_url = []
	list_html = re.findall(r"\bhref=\"//item.jd.com/\b\d+\b.html\b", html_comtent)
	del list_html[:6]
	for i_html in range(0,len(list_html)-1,2):
		list_phone_url.append('https:'+list_html[i_html][6:]+'#comment')
	return list_phone_url

#获取手机名称
def get_phone_name(html):
	list_phone_name = []
	list_phone_name_u = etree.HTML(html.text).xpath('//a[@target="_blank"]//em')
	for i in list_phone_name_u:
		list_phone_name.append(i.text.strip())
	return list_phone_name

#获取手机ID
def get_phone_number(phone_url1):
	list_number = []
	for i_number in phone_url1:
		number = re.findall(r"\d+", i_number)
		list_number.append(number)
	return list_number

#提供评论页数
def get_phone_comment(phone_number1,phone_name1):
	for i_number1 in range(60):
		get_phone_info(phone_number1[i_number1],phone_name1[i_number1])
		time.sleep(0.5)

#获取手机评论信息
def get_phone_info(phone_number_i,phone_name1_i):
	rows=[]
	for i in range(100):
		try:
			#url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8176&productId=5963064&score=0&sortType=5&page=' + str(i) + '&pageSize=20&isShadowSku=0&rid=0&fold=1'
			url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1222&productId=' + phone_number_i[0] +'&score=0&sortType=5&page=' + str(i) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
			r=requests.get(url,headers=headers)
			r=r.text[:-2]
			for j in range(30):
				if (r[j] == u'('):
					b=j+1
			r=r[b:]
			html_parser = HTMLParser.HTMLParser()
			comment_1 = html_parser.unescape(r)
			hjson = json.loads(comment_1)

			get_comment = jsonpath.jsonpath(hjson,"$.comments[*].content")
			#print(type(get_comment[0]))
			get_name = jsonpath.jsonpath(hjson,"$.comments[*].nickname")

			get_creationTime = jsonpath.jsonpath(hjson,"$.comments[*].creationTime")

			get_userLevelName = jsonpath.jsonpath(hjson,"$.comments[*].userLevelName")

			get_usefulVoteCount = jsonpath.jsonpath(hjson,"$.comments[*].usefulVoteCount")

			get_replyCount = jsonpath.jsonpath(hjson,"$.comments[*].replyCount")

			get_score = jsonpath.jsonpath(hjson,"$.comments[*].score")
			try:
				for i_page in range(10):
					if (get_comment[i_page] != u'此用户未填写评价内容'):
						if (';' in get_comment[i_page]):
							get_comment[i_page]=get_comment[i_page].replace(";", ",")
						row=[]
						row.append(get_name[i_page].encode('UTF-8'))
						row.append(get_userLevelName[i_page].encode('UTF-8'))
						row.append(get_comment[i_page].encode('UTF-8'))
						row.append(get_creationTime[i_page])
						row.append(get_usefulVoteCount[i_page])
						row.append(get_replyCount[i_page])
						row.append(get_score[i_page])
						rows.append(row)
						print(get_comment[i_page])
						print('\n')
			except:
				continue
			time.sleep(1.5)
		except:
			break
	#把内容保存为.csv
	with open(phone_name1_i + u'.csv','w') as file:
		file_csv = csv.writer(file)
		file_csv.writerow(e_headers)
		file_csv.writerows(rows)

if __name__ == '__main__':
	for i in range(1,5):
		url = 'https://list.jd.com/list.html?cat=9987,653,655&page=' + str(i) + '&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main'
		html = requests.get(url,headers=headers)
		html_parser = HTMLParser.HTMLParser()
		html_comtent = html_parser.unescape(html.text)
		html_comtent = html_comtent.encode("utf-8")

		phone_url1 = get_phone_url(html_comtent)
		phone_name1 = get_phone_name(html)
		phone_number1 = get_phone_number(phone_url1)

		get_phone_comment(phone_number1,phone_name1)

		time.sleep(0.5)