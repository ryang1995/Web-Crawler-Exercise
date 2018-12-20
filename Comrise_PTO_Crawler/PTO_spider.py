import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

'''
Function: Script for getting PTO time from timesheets for Comrise in-house employees.
Output: saved as "PTO_report.csv" with the same directory with this script.
Author: Rui Yang
Time: September 28, 2018

'''


outputAttr = ['name', 'PTO-Earned', 'PTO-Taken', 'PTO-Remaining', 'PTO-Scheduled']
output = []


def write_to_file():
	# print(content)
	with open('PTO_report.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['name', 'PTO-Earned', 'PTO-Taken', 'PTO-Remaining', 'PTO-Scheduled'])
		
		for content in output:
			writer.writerow([content[attr] for attr in outputAttr])

		# f.write(json.dumps(content, ensure_ascii=False) + '\n')


def parse_PTO_time(html):
	# print(html)
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find_all('table', {'class':'table-bordered'})
	attrDict = defaultdict(dict)
	if len(table) > 1:
		PTO_data = table[1].find('tbody').find('tr').find_all('td')
		for i in range(1, len(outputAttr)):
			attrDict[outputAttr[i]] = PTO_data[i].text
	else:
		for i in range(1, len(outputAttr)):
			attrDict[outputAttr[i]] = "Don't have"
	return attrDict

'''
Function to get offset of url for each employee from timesheets.
'''
def parse_url_from_timesheet(session, html):
	soup = BeautifulSoup(html, 'html.parser')
	inhouse_data = soup.find('tbody').find_all('tr')
	for item in inhouse_data:
		if item.find('span', {'class':'label-danger'}):
			pass
		else :
			# get the offset url from timesheets
			name_tag = item.find_all('td')[1].find('a')
			offset = name_tag.get('href')
			# Get offset, request new pate
			html = get_one_page(session, offset)
			if not html is None:
				# attrDict = defaultdict(dict)
				attrDict = parse_PTO_time(html)
				attrDict['name'] = name_tag.text.strip()
				output.append(attrDict)

def get_one_page(session, offset):
	try:
		response = session.get("http://52.3.238.236/admin/timesheets/" + offset)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException as e:
		return None

def login():
	session = requests.session()

	login_data = {
		'username': 'USERNAME',
		'password': 'PASSWORD',
		'action': 'login'
	}

	session.post('http://52.3.238.236/index.php', data=login_data)
	return session

if __name__ == '__main__':

	session = login()
	html = get_one_page(session, "index.php?type=in-house") 

	if not html is None:
		parse_url_from_timesheet(session, html)

	write_to_file()





