#download temperature data from usclimatedata.com
import urllib
from bs4 import BeautifulSoup
import json

year=range(2005,2014)
month=range(1,13)
record={}

def get_table(y,m):
	adr='http://www.usclimatedata.com/climate/pampa/texas/united-states/ustx1017/'+str(y)+'/'+str(m)
	http=urllib.urlopen(adr)
	text=http.read()
	soup=BeautifulSoup(text)
	text=soup.find('div',{'id':'history_data'})
	soup=BeautifulSoup(str(text))
	day=soup.find_all('td',{'class':'align_left daily_climate_table_td_day'})
	high=soup.find_all('td',{'class':'align_right climate_table_data_td temperature_red '})
	low=soup.find_all('td',{'class':'align_right climate_table_data_td temperature_blue'})
	other_three=soup.find_all('td',{'class':'align_right climate_table_data_td'})
	record={}
	month=str(m)
	if m<10:
		month='0'+month
	for i in range(0,len(day)):
		if i<9:
			date=str(y)+month+'0'+str(i+1)
		else:
			date=str(y)+month+str(i+1)
		record[date]={
					'high':high[i].string.encode('utf'),
					'low':low[i].string.encode('utf'),
					'preception':other_three[3*i].string.encode('utf')
					}
	return(record)

for y in year:
	for m in month:
		print y,m
		record.update(get_table(y,m))
f=open('/Users/sheepfriend/data.csv','w')
f.write("'date';'high';'low';'preception'\n")
for key in sorted(record):
	value=record[key]
	f.write(key+";"+value['high']+";"+value['low']+";"+value['preception']+"\n")
f.close()
