#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,re,ch,os
from datetime import datetime

urls=[]

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt','r')
time_zone = fil.read().strip()
fil.close()

for i in range(0,5):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('https://www.dstv.co.za/webmethods/no-cache/GetChannelAllDate.ashx?d='+str(week)+'')

with io.open("/etc/epgimport/dstv.xml","w",encoding='UTF-8')as f:
    f.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
for cc in ch.ZA:
    with io.open("/etc/epgimport/dstv.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+cc+'">'+"\n"+'    <display-name lang="en">'+cc+'</display-name>'+"\n"+'  </channel>'+"\r").decode('utf-8'))

def dstv():
    for url in urls:
        link = requests.get(url,headers=headers)
        data=json.loads(link.text)
        for d in data['Channels']:
            for prog in d['Programmes']:
                ch=''
                startime= datetime.datetime.strptime(prog['StartTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                endtime= datetime.datetime.strptime(prog['EndTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                ch+=2*' '+'<programme start="'+startime+' '+time_zone+'" stop="'+endtime+' '+time_zone+'" channel="'+d['Name'].replace(' ','').replace('&','and')+'">\n'
                ch+=4*' '+'<title lang="en">'+prog['Title'].replace('&','and')+'</title>\n'
                ch+=4*' '+'<desc lang="en">'+prog['Title'].replace('&','and')+'</desc>\n  </programme>\r'
                with io.open("/etc/epgimport/dstv.xml","a",encoding='UTF-8')as f:
                    f.write(ch)
        dat = re.search(r'\d{4}-\d{2}-\d{2}',url)
        print('Date'+' : '+dat.group())    

if __name__=='__main__':
    dstv()


with io.open("/etc/epgimport/dstv.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
    
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.channels.xml?raw=true -O /etc/epgimport/custom.channels.xml')
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.sources.xml?raw=true -O /etc/epgimport/custom.sources.xml')


if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true -O /etc/epgimport/elcinema.channels.xml')

if not os.path.exists('/etc/epgimport/dstv.channels.xml'):
    print('Downloading dstv channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true -O /etc/epgimport/elcinema.channels.xml')
