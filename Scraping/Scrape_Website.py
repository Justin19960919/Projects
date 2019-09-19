'''
page1 = "https://www.xvideos.com"
resp = requests.get(page1)
soup = BeautifulSoup(resp.text, 'html.parser')

soup_div=soup.select('div > .thumb-under > p > a')
print(list(map(lambda x: x.find('href'),soup_div)))
'''
# -!- coding: utf-8 -!-

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from multiprocessing import Pool
from functools import reduce
### ------ importing self -defined function ------
#import FunctionLib



## try exceapt
## import logging
## multiprocessing

all_links = ['https://www.xvideos.com/new/'+str(i) for i in range(1,20000)]
all_links =['https://www.xvideos.com']+all_links
#print(all_links)
def ToSeconds(mytimee):
	mytimee=mytimee.lower()
	mytimee=mytimee.replace("min","m")
	mytimee=mytimee.replace("sec","s")
	mytimee=mytimee.split(" ")
	final = 0
	for mt in mytimee:
		if mt not in ["h","m","s"]:
			temp_num=int(mt)
		else:
			if mt=="h":
				grid = 3600
			elif mt =="m":
				grid = 60
			elif mt =="s":
				grid = 1
			final += temp_num*grid

	return final





def ScrapeAPage(url):
	try:
		resp = requests.get(url)
		if resp.status_code == 200:

			print("========= Access success....========= ")
			soup = BeautifulSoup(resp.text, 'html.parser')
			## prepare container for scraping data
			page = []
			div_test = soup.find_all("div","thumb-under")

			# Get all on first page
			for dvt in div_test:

				# get url
				geturl = dvt.find("a")['href']
				# get title
				title = dvt.find("a")['title']
				## prepare time author views
				info = dvt.find("p","metadata") 
				## get time
				time_length = info.find("span","duration").text
				# modify time 
				time_length = ToSeconds(time_length)

				## got author
				author = info.find("span","name").text
				## get Views
				spr=info.find_all("span") 
				
				for sp in spr:
					div_text =sp.get_text()
					## returns a list of text
					
					if div_text.find("Views")!=(-1):

						div_text = div_text.replace("-","")
						div_text = div_text.replace("Views","")
						div_text = div_text.replace(" ","")
						div_text = div_text.lower()
						
						#text.append(div_text)
						if (len(div_text)<10) & (len(div_text)>0):
							
							if div_text[-1]=="k":
								multiply_by = 10**3
							elif div_text[-1]=="m":
								multiply_by = 10**6
							elif div_text[-1]=="g":
								multiply_by = 10**9
							elif div_text[-1]=="t":
								multiply_by = 10**12
							elif div_text[-1]=="p":
								multiply_by = 10**15
							elif div_text[-1]=="e":
								multiply_by = 10**18

							#Views_number = [div_text,int(float(div_text[:-1])*multiply_by)]
							Views_number = int(float(div_text[:-1])*multiply_by)

				page.append({"url":geturl,"title":title,"time":time_length,"author":author,"Views":Views_number})

			end_time = time.time()
			print("Executing",url,".....")

			#print("Used up",format(used_time,".2E"),"secs...")
			print("========= Scraping success....========= ")

			return page
			time.sleep(1)
	
	except Exception as ex:
		print('Error: ',str(ex))
		print("========= Scraping failed....========= ")
		pass




def fn(x, y):
	return x+y





def Pages(pool_v,page):

	test_links = all_links[:page]
	start_time = time.time()
	with Pool(pool_v) as p:
		records=p.map(ScrapeAPage,test_links)

	p.terminate()
	p.join()
	end_time= time.time()
	print("Used up",format(end_time-start_time,".2E"),"secs...")

	records = reduce(fn, records)  ## merging lists among lists
	print(len(records))

	xv_df=pd.DataFrame(records,columns=["url","title","time","author","Views"])
	xv_df=xv_df.sort_values("Views",ascending=False)


	xv_df.to_csv('/Users/justin/Desktop/xv.csv',index=False,sep=",")



# for scraping ---
Pages(1,1)
































































