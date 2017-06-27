# -*- coding: utf-8 -*-

import time
from bs4 import BeautifulSoup

from mylog import *
from open_url import *

FLAG_base_url = "http://zu.xian.fang.com/house"
FLAG_page_from = 1
FLAG_page_to = 101

# 下面这组函数, 输入的 bs 对象, 都是到 list rel 这一级的, 也就是每一个房源的最高级别对象
def GetTitle(item):
	return item.find_all(class_ = "title")[0].a.attrs["title"]

def GetEntry(item):
	return item.find_all(class_ = "title")[0].a.attrs["href"]

def GetRooms(item):
	'''
	获取户型信息
	'''
	return item.find_all(class_ = "font16 mt20 bold")[0].contents[2].strip()

def GetHeight(item):
	'''
	获取楼层总高度
	'''
	return item.find_all(class_ = "font16 mt20 bold")[0].contents[6].strip()

def GetPlotName(item):
	'''
	获取小区名字
	'''
	return item.find_all(class_ = "gray6 mt20")[0].contents[-2].span.string
	#return item.find_all(class_ = "gray6 mt20")[0].contents

def GetPlotUrl(item):
	'''
	获取小区 url
	'''
	return item.find_all(class_ = "gray6 mt20")[0].contents[-2].attrs["href"]

def GetArea(item):
	'''
	获取面积
	'''
	return item.find_all(class_ = "font16 mt20 bold")[0].contents[4].strip()

def GetTotalPrice(item):
	'''
	获取总价
	'''
	return ""

def GetUnitPrice(item):
	'''
	获取单价
	'''
	return item.find_all(class_ = "price")[0].string

def GetTrainNote(item):
	'''
	获取地铁信息
	'''
	result = item.find_all(class_ = "note subInfor")
	if len(result) == 0:
		return ""
	return result[0].contents[0].string + result[0].contents[1].string + result[0].contents[2].string

def GetResult(item):
	title = GetTitle(item)
	entry = GetEntry(item)
	rooms = GetRooms(item)
	height = GetHeight(item)
	year = ""
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

def GetItemList(main_url):
	page = OpenGzipPageRetry(main_url)
	soup = BeautifulSoup(page, 'html.parser')
	rel_list = soup.find_all(class_ = "info rel")
	return rel_list

def GetUrlList(main_url):
	item_list = GetItemList(main_url)
	result_list = []
	for item in item_list:
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
	global FLAG_base_url
	base_url = FLAG_base_url
	if page == 1:
		return base_url + "/n31"
	return base_url + "-i3" + str(page) + "-n31"

def CrawlerAllUrlList():
	local_time = time.localtime()
	url_list = []
	global FLAG_page_from
	global FLAG_page_to
	for page in range(FLAG_page_from, FLAG_page_to):
		main_url = GenMainUrlByPage(page)
		Log(INFO, "crawler start! " + main_url)
		url_list.extend(GetUrlList(main_url))
		Log(INFO, "crawler done!")
	Log(INFO, "writing start!")
	WriteUrlList("zufang_", url_list, local_time)
	Log(INFO, "writing done!")

def TestMain():
	url = GenMainUrlByPage(1)
	item_list = GetItemList(url)
	for item in item_list:
		#Log(INFO, str(GetTitle(item)))
		#Log(INFO, str(GetEntry(item)))
		#Log(INFO, str(GetRooms(item)))
		#Log(INFO, str(GetHeight(item)))
		#Log(INFO, str(GetArea(item)))
		Log(INFO, str(GetPlotName(item)))
		#Log(INFO, str(GetPlotUrl(item)))
		#Log(INFO, str(GetUnitPrice(item)))
		#Log(INFO, str(GetTrainNote(item)))
		pass

if __name__ == "__main__":
	CrawlerAllUrlList()
	#TestMain()