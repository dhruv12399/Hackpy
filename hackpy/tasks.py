from __future__ import absolute_import

from hackpy.celery import app
import requests
from bs4 import BeautifulSoup
import sys
from django.contrib.auth.models import User
from hackernews.models import Link, Comments 
import datetime
from django.utils import timezone
from celery import Celery

@app.task
def ScanPage(i):
	reload(sys)
	sys.setdefaultencoding('utf8')
	url = 'https://news.ycombinator.com/news?p='+str(i)
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	# print soup.prettify()
	l_list = soup.find_all("tr", class_="athing")
	s_list = soup.find_all("td", class_="subtext")
	for i in range(30):
		CrawlLink.delay(i,l_list, s_list)

@app.task
def CrawlLink(i, l_list, s_list):
	l_title = l_list[i].find_all("a", class_="storylink")[0].get_text()
	l_url = l_list[i].find_all('a',href=True ,class_="storylink")[0]['href']
	l_parent = l_list[i].find_all("span", class_="sitestr")
	if len(l_parent)==0:
		return
	else:
		l_parent = l_parent[0].get_text()
	l_votes = int(s_list[i].find_all('span',class_="score")[0].get_text().split(' ')[0])
	l_username = s_list[i].find_all("a", class_="hnuser")[0].get_text()
	y = int(s_list[i].find_all('span', class_='age')[0].get_text().split(' ')[0])
	x = s_list[i].find_all('span', class_='age')[0].get_text().split(' ')[1]
	l_added_time = timezone.now()
	if x == 'hours':
		l_added_time = timezone.now() - datetime.timedelta(hours = y)
	elif x == 'minutes':
		l_added_time = timezone.now() - datetime.timedelta(minutes = y)
	elif x == 'days':
		l_added_time = timezone.now() - datetime.timedelta(days = y)

	if User.objects.filter(username=l_username).exists():
		l_user = User.objects.filter(username=l_username)[0]
	else:
		l_user = User.objects.create_user(username=l_username)

	if Link.objects.filter(url = l_url).exists():
		l = Link.objects.filter(url = l_url)[0]
	else:
		l = Link(title = l_title, url = l_url, parent = l_parent, votes = l_votes, added_by = l_user, added_time = l_added_time)
		l.save()
	print l_title," crawled succesfuly"
	l_comment_url = 'https://news.ycombinator.com/' + s_list[i].find_all('a')[-1]['href']
	page_c = requests.get(l_comment_url)
	soup_c = BeautifulSoup(page_c.text, 'html.parser')
	c_list = soup_c.find_all('tr',class_='comtr')
	for c in c_list:
		CrawlComment.delay(c,l)

@app.task
def CrawlComment(c,l):
	width = int(c.find_all('img')[0]['width'])
	if width!=0:
		return
	s = c.find_all('span', class_='c00')
	if not s:
		return
	s = s[0]
	s = str(s)
	start = s.find('c00')+5
	end = s.find('<span>',start)
	l_comment_content = s[start:end]
	l_comment_username = c.find_all('a', class_='hnuser')[0].get_text()
	if User.objects.filter(username=l_comment_username).exists():
		l_comment_user = User.objects.filter(username=l_comment_username)[0]
	else:
		l_comment_user = User.objects.create_user(username=l_comment_username)

	if Comments.objects.filter(content = l_comment_content).exists():
		p = Comments.objects.filter(content = l_comment_content)[0]
	else:
		p = Comments(content = l_comment_content, linked_to = l, added_by = l_comment_user, parent = None)
		p.save()
	print l_comment_username, "crawled succesfuly"