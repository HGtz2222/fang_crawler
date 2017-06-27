# -*- coding: utf-8 -*-

import gzip
import urllib.request
import io

from mylog import *

request = urllib.request

def OpenGzipPage(main_url):
	'''
	有些网站的页面是通过 gzip 来压缩的, 拿到网页需要
	先进行解压缩. 解压缩的步骤是固定的.
	'''
	req = request.Request(main_url)
	req.add_header('Accept-encoding', 'gzip')
	response = request.urlopen(req)
	if response.info().get('Content-Encoding') != 'gzip':
		Log(ERROR, "page encoding error! not gzip")
		return
	buf = io.BytesIO(response.read())
	f = gzip.GzipFile(fileobj = buf, mode = 'rb')
	main_page = f.read().decode('gbk')
	response.close()
	return main_page

def OpenGzipPageRetry(main_url):
	for i in range(0, 3):
		main_page = ""
		try:
			main_page = OpenGzipPage(main_url)
		except Exception as e:
			Log(ERROR, str(e))
		if len(main_page) > 0:
			return main_page
	Log(ERROR, "retry 3 times error!")
	return ""