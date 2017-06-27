# -*- coding: utf-8 -*-

import time
from bs4 import BeautifulSoup

from mylog import *
from open_url import *

# 下面这组函数, 输入的 bs 对象, 都是到 list rel 这一级的, 也就是每一个房源的最高级别对象
def GetTitle(item):
	return item.find_all(class_ = "title")[0].a.attrs["title"]

def GetEntry(item):
	return item.find_all(class_ = "title")[0].a.attrs["href"]

def GetRooms(item):
	'''
	获取户型信息
	'''
	return item.find_all(class_ = "mt12")[0].contents[0].strip()

def GetHeight(item):
	'''
	获取楼层总高度
	'''
	return item.find_all(class_ = "mt12")[0].contents[2].strip()

def GetYear(item):
	'''
	获取房龄
	'''
	return item.find_all(class_ = "mt12")[0].contents[-1].strip()

def GetPlotName(item):
	'''
	获取小区名字
	'''
	return item.find_all(class_ = "mt10")[0].a.attrs["title"]

def GetPlotUrl(item):
	'''
	获取小区名字
	'''
	return item.find_all(class_ = "mt10")[0].a.attrs["href"]

def GetArea(item):
	'''
	获取面积
	'''
	return item.find_all(class_ = "area alignR")[0].contents[1].string

def GetTotalPrice(item):
	'''
	获取总价
	'''
	return item.find_all(class_ = "price")[0].string

def GetUnitPrice(item):
	'''
	获取单价
	'''
	return item.find_all(class_ = "danjia alignR mt5")[0].contents[0].string

def GetTrainNote(item):
	'''
	获取地铁信息
	'''
	result = item.find_all(class_ = "train note")
	if len(result) == 0:
		return ""
	return result[0].string

def GetResult(item):
	title = GetTitle(item)
	entry = GetEntry(item)
	rooms = GetRooms(item)
	height = GetHeight(item)
	year = GetYear(item)
	plot_name = GetPlotName(item)
	plot_url = GetPlotUrl(item)
	area = GetArea(item)
	total_price = GetTotalPrice(item)
	unit_price = GetUnitPrice(item)
	train_note = GetTrainNote(item)

	result = {
		"title" : title,
		"entry" : entry,
		"rooms" : rooms,
		"height" : height,
		"year" : year,
		"plot_name" : plot_name,
		"plot_url" : plot_url,
		"area" : area,
		"total_price" : total_price,
		"unit_price" : unit_price,
		"train_note" : train_note
	}
	return result

def GetUrlList(main_url):
	page = OpenGzipPageRetry(main_url)
	soup = BeautifulSoup(page, 'html.parser')
	rel_list = soup.find_all(class_ = "list rel")
	result_list = []
	for item in rel_list:
		result = GetResult(item)
		result_list.append(result)
	return result_list

def ItemToString(url):
	line = url["entry"] + "\t" + url["title"] + "\t" + url["rooms"] + "\t" \
		+ url["height"] + "\t" + url["year"] + "\t" + url["plot_name"] + "\t" \
		+ url["plot_url"] + "\t" + url["area"] + "\t" + url["total_price"] + "\t" \
		+ url["area"] + "\t" + url["total_price"] + "\t" + url["unit_price"] + "\t" \
		+ url["train_note"] + "\n"
	return line

def WriteUrlList(file_prefix, url_list, local_time):
	fp = open(file_prefix + str(time.strftime("%Y%m%d_%H%M%S", local_time)) + ".txt", 'wt+')
	for url in url_list:
		line = ""
		try:
			line = ItemToString(url)
		except Exception as e:
			Log(ERROR, "item error! " + str(e) + "\n" + str(url))
			continue
		fp.write(line)
	fp.close()

def GenMainUrlByPage(page):
	if page < 1 or page > 100:
		return ""
	base_url = "http://esf.xian.fang.com/house/c230-d250-r22-s25-h316"
	if page == 1:
		return base_url
	return base_url + "-i3" + str(page)

def CrawlerAllUrlList():
	local_time = time.localtime()
	url_list = []
	for page in range(1, 101):
		main_url = GenMainUrlByPage(page)
		Log(INFO, "crawler start! " + main_url)
		url_list.extend(GetUrlList(main_url))
		Log(INFO, "crawler done!")
	Log(INFO, "writing start!")
	WriteUrlList("maifang_", url_list, local_time)
	Log(INFO, "writing done!")

if __name__ == "__main__":
	CrawlerAllUrlList()