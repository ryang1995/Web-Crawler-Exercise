import re
import random
import requests
from bs4 import BeautifulSoup

base_url = "https://en.wikipedia.org"
# list to save all the offset of urls the crawler went to
his = ["/wiki/web_crawler"]

for i in range(20):
	url = base_url + his[-1]
	html = requests.get(url).text

	soup = BeautifulSoup(html, 'html.parser')

	print(soup.find('h1').get_text(),  '\t\turl: ', his[-1])

	# Get all the possible link from page
	offsets = soup.find("div",{"id": "mw-content-text"}).find_all("a", {"href": re.compile(r"(^/wiki/)")})
	# for link in offsets
	# 	print(link.get('href'))

	# Randomly choose a url offset from offsets list
	if len(offsets) != 0:
	    his.append(random.sample(offsets, 1)[0].get('href'))
	else:
	    # no valid sub link found
	    his.pop()
	# print(his)