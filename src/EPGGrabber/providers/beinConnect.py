#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
	from .__init__ import *
except:
	from __init__ import *

import re
import sys
import io
import json
from datetime import timedelta
from time import strftime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import datetime
week = datetime.date.today() + timedelta(days=7)
from datetime import datetime
milli = (datetime.strptime('' + str(week) + ' 23:59:59', "%Y-%m-%d %H:%M:%S").strftime("%s")) + '.999'
today = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime('%s')

ch_code = ['74-beIN Sports', '75-beIN Sports News', '67-beIN 1HD', '70-beIN 2HD', '68-beIN 3HD', '69-beIN 4HD',
           '73-beIN 5HD', '71-beIN 6HD', '58-beIN 7HD', '65-beIN 1 PREM', '66-beIN 2 PREM', '72-beIN 3 PREM',
           '103-beIN SPORTS XTRA 1', '104-beIN SPORTS XTRA 2', '59-beIN 1HD english', '60-beIN 2HD english',
           '61-beIN 3HD english', '62-beIN SPORTS 1 FR', '63-beIN SPORTS 2 FR', '64-beIN SPORTS 3 FR']
# '101-beIN SPORTS MAX 1', '102-beIN SPORTS MAX 2', '216-beIN SPORTS MAX 3','217-beIN SPORTS MAX 4','213-beIN SPORTS MAX 5','218-beIN SPORTS MAX 6'

head = {
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	"x-an-webservice-identitykey": "t1Th55UviStev8p2urOv4fOtraDaBr1f"
}


time_zone = tz()


def b_connect():
	print('**************BEIN SPORTS CONNECT EPG******************')
	sys.stdout.flush()
	for code in ch_code:
		query = {
			"languageId": "ara",
			"filter": '{"$and":[{"id_channel":{"$in":[' + code.split('-')[0] + ']}},{"endutc":{"$ge":' + today + '}},{"startutc":{"$le":' + milli + '}}]}'
		}
		url = requests.get('https://proxies-beinmena.portail.alphanetworks.be/cms/epg/filtered', headers=head, params=query, verify=False).json()
		if url['status'] == False:
			print('Invalid API Key')
			break
		else:
			for data in url['result']['epg']['chan_' + code.split('-')[0]]:
				start = datetime.fromtimestamp(int(data['startutc'])).strftime('%Y%m%d%H%M%S')
				end = datetime.fromtimestamp(int(data['endutc'])).strftime('%Y%m%d%H%M%S')
				title = data['title'].replace('   ', ' ').split('- ')[0]
				if PY3:
					if 'Qatar Stars League' in data['title']:
							extra = 'دوري نجوم قطر'
					elif 'Moroccan League' in data['title']:
							extra = 'الدوري المغربي الممتاز'
					elif 'Review' in data['title']:
							extra = 'حصيلة الدوريات'
					elif 'English Premier League' in data['title']:
							extra = 'الدوري الإنجليزي الممتاز'
					elif 'Spanish La Liga' in data['title'] or 'La Liga World' in data['title'] or 'La Liga Show' in data['title']:
							extra = 'الدوري الإسباني لكرة القدم'
					elif 'Italian Serie A' in data['title']:
							extra = 'الدوري الإيطالي لكرة القدم'
					elif 'French Ligue 1' in data['title'] or 'Ligue 1 Weekly Preview' in data['title']:
							extra = 'الدوري الفرنسي'
					elif 'Copa Libertadores' in data['title']:
							extra = 'كأس ليبرتادوريس'
					elif 'Indy' in data['title']:
							extra = 'رياضة السيارات'
					elif 'MotoGP' in data['title']:
							extra = 'بطولة العالم للدراجات النارية'
					elif 'Pre Season Friendly' in data['title']:
							extra = 'كرة قدم'
					elif 'NBA' in data['title']:
							extra = 'الدوري الأميركي لكرة السلة'
					elif 'WTA' in data['title'] or 'Tennis' in data['synopsis']:
							extra = 'تنس'
					elif 'Mini Match' in data['title']:
							extra = 'مباريات قصيرة'
					elif 'Major League Baseball' in data['title']:
							extra = 'كرة القاعدة'
					elif 'UEFA Champions League' in data['title'] or 'UEFA Highlights' in data['title']:
							extra = 'دوري أبطال أوروبا لكرة القدم'
					elif 'UEFA Europa League' in data['title']:
							extra = 'الدوري الأوروبي'
					elif 'Cricket' in data['title']:
							extra = 'كريكيت'
					elif 'Sports News' in data['title']:
							extra = 'الأخبار الرياضية'
					elif 'Handball' in data['title']:
							extra = 'كرة اليد'
					elif 'EPL World' in data['title'] or 'EPL Matchpack' in data['title']:
							extra = 'عالم الدوري الانجليزي الممتاز'
					elif 'CAF Champions League' in data['title'] or "CAF Champion's League" in data['title']:
							extra = 'دوري أبطال أفريقيا'
					else:
							extra = 'الرياضة العام'
				else:
					if 'Qatar Stars League' in data['title']:
							extra = 'دوري نجوم قطر'.decode('utf-8')
					elif 'Moroccan League' in data['title']:
							extra = 'الدوري المغربي الممتاز'.decode('utf-8')
					elif 'Review' in data['title']:
							extra = 'حصيلة الدوريات'.decode('utf-8')
					elif 'English Premier League' in data['title']:
							extra = 'الدوري الإنجليزي الممتاز'.decode('utf-8')
					elif 'Spanish La Liga' in data['title'] or 'La Liga World' in data['title'] or 'La Liga Show' in data['title']:
							extra = 'الدوري الإسباني لكرة القدم'.decode('utf-8')
					elif 'Italian Serie A' in data['title']:
							extra = 'الدوري الإيطالي لكرة القدم'.decode('utf-8')
					elif 'French Ligue 1' in data['title'] or 'Ligue 1 Weekly Preview' in data['title']:
							extra = 'الدوري الفرنسي'.decode('utf-8')
					elif 'Copa Libertadores' in data['title']:
							extra = 'كأس ليبرتادوريس'.decode('utf-8')
					elif 'Indy' in data['title']:
							extra = 'رياضة السيارات'.decode('utf-8')
					elif 'MotoGP' in data['title']:
							extra = 'بطولة العالم للدراجات النارية'.decode('utf-8')
					elif 'Pre Season Friendly' in data['title']:
							extra = 'كرة قدم'.decode('utf-8')
					elif 'NBA' in data['title']:
							extra = 'الدوري الأميركي لكرة السلة'.decode('utf-8')
					elif 'WTA' in data['title'] or 'Tennis' in data['synopsis']:
							extra = 'تنس'.decode('utf-8')
					elif 'Mini Match' in data['title']:
							extra = 'مباريات قصيرة'.decode('utf-8')
					elif 'Major League Baseball' in data['title']:
							extra = 'كرة القاعدة'.decode('utf-8')
					elif 'UEFA Champions League' in data['title'] or 'UEFA Highlights' in data['title']:
							extra = 'دوري أبطال أوروبا لكرة القدم'.decode('utf-8')
					elif 'UEFA Europa League' in data['title']:
							extra = 'الدوري الأوروبي'.decode('utf-8')
					elif 'Cricket' in data['title']:
							extra = 'كريكيت'.decode('utf-8')
					elif 'Sports News' in data['title']:
							extra = 'الأخبار الرياضية'.decode('utf-8')
					elif 'Handball' in data['title']:
							extra = 'كرة اليد'.decode('utf-8')
					elif 'EPL World' in data['title'] or 'EPL Matchpack' in data['title']:
							extra = 'عالم الدوري الانجليزي الممتاز'.decode('utf-8')
					elif 'CAF Champions League' in data['title'] or "CAF Champion's League" in data['title']:
							extra = 'دوري أبطال أفريقيا'.decode('utf-8')
					else:
							extra = 'الرياضة العام'.decode('utf-8')
				spl = re.search(r'-\s(.*)', title)
				ch = ''
				ch += 2 * ' ' + '<programme start="' + start + ' ' + time_zone + '" stop="' + end + ' ' + time_zone + '" channel="' + code.split('-')[1] + '">\n'
				if spl != None:
					ch += 4 * ' ' + '<title lang="en">' + spl.group().replace('&', 'and') + ' - ' + extra + '</title>\n'
				else:
					ch += 4 * ' ' + '<title lang="en">' + title.replace('&', 'and').strip() + ' - ' + extra + '</title>\n'
				if data['synopsis'].strip() == '' and ' -' in data['title']:
					ch += 4 * ' ' + '<desc lang="en">' + data['title'].split(' -')[1].strip().replace('&', 'and') + '</desc>\n  </programme>\r'
				elif data['synopsis'].strip() == '':
					ch += 4 * ' ' + '<desc lang="en">' + title.replace('&', 'and') + '</desc>\n  </programme>\r'
				else:
					ch += 4 * ' ' + '<desc lang="en">' + data['synopsis'].strip().replace('&', 'and') + '</desc>\n  </programme>\r'
				endtime = datetime.strptime(start, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')

				with io.open(EPG_ROOT + '/beinConnect.xml', 'a', encoding="utf-8") as f:
					f.write(ch)
			print(code.split('-')[1] + ' epg ends at ' + endtime)
			sys.stdout.flush()


def main():
	channels = [ch.split('-')[1] for ch in ch_code]
	xml_header(EPG_ROOT + '/beinConnect.xml', channels)

	b_connect()

	close_xml(EPG_ROOT + '/beinConnect.xml')

	with open(PROVIDERS_ROOT, 'r') as f:
		data = json.load(f)
	for bouquet in data['bouquets']:
		if bouquet["bouquet"] == "beinConnect":
			bouquet['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
			with open(PROVIDERS_ROOT, 'w') as f:
				json.dump(data, f)

	print("**************FINISHED******************")
	sys.stdout.flush()


if __name__ == "__main__":
	main()
