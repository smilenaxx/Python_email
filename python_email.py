from datetime import datetime
import requests
from bs4 import BeautifulSoup as BS
import re

#获取html的soup
def get_htmlsoup(url):
	r = requests.get(url)
	soup = BS(r.text,"html.parser")
	return soup
#获取时间
def get_time():
	now = datetime.now()
	today_time = str(now.strftime('%Y年%m月%d日 %A'))
	return today_time
#获取地区
def get_title(soup):
	soup_title = BS(str(soup.find_all('div',"btitle")[0]),"html.parser")
	weather_title = soup_title.h1.string
	return weather_title
#获取天气状况
def get_weather(soup):
	day_soup = BS(str(soup.find_all("dl","day")),"html.parser")
	night_soup = BS(str(soup.find_all("dl","night")),"html.parser")
	parameter_soup = BS(str(soup.find_all("ul","parameter")),"html.parser")

	#白天天气状况,str
	day_title = day_soup.dt.get_text()
	day_status = BS(str(day_soup.find_all('span','phrase')),"html.parser").span.get_text()
	day_temp = BS(str(day_soup.find_all('span','temperature')),"html.parser").get_text()[1:-1]
	day_list = [day_title+':'+day_status,day_temp]

	#夜晚天气状况,str
	night_title = night_soup.dt.get_text()
	night_status = BS(str(night_soup.find_all('span','phrase')),"html.parser").span.get_text()
	night_temp = BS(str(night_soup.find_all('span','temperature')),"html.parser").get_text()[1:-1]
	night_list = [night_title+':'+night_status,night_temp]

	#空气参数,list
	para_key = parameter_soup.find_all('b')
	para_value = parameter_soup.find_all('i')

	para_list = []
	for i in [1,2,3,4,6,8,9]:
		para_list.append(para_key[i].get_text() + para_value[i].get_text())

	weather_list = [day_list,night_list,para_list]
	return weather_list
#获取空气质量
def get_airquality(soup):
	air_title = BS(str(soup.find_all('div','stitle')),'html.parser').h3.contents[0][0:-2]
	air_quality_key = BS(str(soup.find_all('div','standard')),'html.parser').find_all('td','td-1')[4].get_text()
	air_quatily_value = BS(str(soup.find_all('div','standard')),'html.parser').find_all('td','td-2')[4].get_text()
	air_quality = air_quality_key + ':' + air_quatily_value
	air_remind_list = [x.get_text() for x in BS(str(soup.find_all
					('div','remindarea clearfix')),'html.parser').find_all('p','rules')]
	air_list = [air_title,air_quality,air_remind_list]
	return air_list
#获取星座url（天蝎）
def get_constellation_url():
	#正则
	p = re.compile('"[^"]*"\s')
	#日期
	now = datetime.now()
	today_time = str(now.strftime('%m月%d日'))
	time_list = list(today_time)
	if '0' == time_list[3]:
		time_list.pop(3)
	if '0' == time_list[0]:
		time_list.pop(0)
	today_time = ''.join(time_list)
	#url
	r = requests.get("http://www.meiguoshenpo.com/tianxie/yunshi/jinri.html")
	soup = BS(r.text,"html.parser")
	for i in BS(str(soup.find_all('div','list_item')),'html.parser').find_all('h4'):
		if today_time in str(i) and '天蝎座' in str(i):
			today_url = p.findall(str(i))

	return today_url[0][0:-1]
#获取星座运势
def get_constellation(soup):
	#正则
	p1 = re.compile('</*p>|</*strong>') 
	p2 = re.compile('<br/')

	cons_soup = soup
	cons_list = []
	for x in BS(str(cons_soup.find_all('div','show_cnt')),'html.parser').find_all('p'):
		cons_list.append(p1.sub('',str(x)))
	cons_list = [cons_list[1],cons_list[2],cons_list[3]]
	for i in range(len(cons_list)):
		cons_list[i] = cons_list[i].replace('<br/>','\n')
	
	return cons_list



#主函数(暂时)
def main():
	#时间部分
	today_time = get_time()
	
	#天气部分
	weather_url = "http://tianqi.2345.com/today-58238.htm"
	weather_soup = get_htmlsoup(weather_url)
	
	weather_title = get_title(weather_soup)
	weather_list = get_weather(weather_soup)
	day_list = '  '.join(weather_list[0])
	night_list = '  '.join(weather_list[1])
	para_list = '\n'.join(weather_list[2])

	#空气质量部分
	air_url = "http://tianqi.2345.com/air-58238.htm"
	air_soup = get_htmlsoup(air_url)
	
	air_title = get_airquality(air_soup)[0]
	air_quality = get_airquality(air_soup)[1]
	air_remind = ' & '.join(get_airquality(air_soup)[2])

	#星座部分
	cons_url = get_constellation_url()[1:-1]
	cons_soup = get_htmlsoup(cons_url)
	cons_list = get_constellation(cons_soup)

	#输出检测
	print(today_time+'\n')
	print(weather_title+'\n'+day_list+'\n'+night_list+'\n'+para_list+'\n')
	print(air_title+'\n'+air_quality+'\n'+air_remind+'\n')
	for x in cons_list:
		print(x)

if __name__ == '__main__':	  
	main()






