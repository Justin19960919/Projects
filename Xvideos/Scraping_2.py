'''
page1 = "https://www.xvideos.com"
resp = requests.get(page1)
soup = BeautifulSoup(resp.text, 'html.parser')

soup_div=soup.select('div > .thumb-under > p > a')
print(list(map(lambda x: x.find('href'),soup_div)))
'''
# -!- coding: utf-8 -!-

import requests
from bs4 import BeautifulSoup ## 從bs4 packagae import BeautifulSoup function 所以可以直接用
import time
import pandas as pd
import numpy as np
from multiprocessing import Pool
from functools import reduce
import matplotlib.pyplot as plt
### ------ importing self -defined function ------
#import FunctionLib



## try except
## import logging
## multiprocessing

all_links = ['https://www.xvideos.com/new/'+str(i) for i in range(1,20000)]
all_links =['https://www.xvideos.com']+all_links
#print(all_links)

def ToMins(mytimee):
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
				grid = 60
			elif mt =="m":
				grid = 1
			elif mt =="s":
				grid = 1/60
			final += temp_num*grid

	return round(final,2)

def ToNumberViews(views):

	views_dict={"k":10**3,"m":10**6,"g":10**9,"t":10**12,"p":10**15,"e":10**18}

	if views[-1] not in ["k","m","g","t","p","e"]:
		try:	
			Views_result=int(views)
		except ValueError as ve:
			print("Error ",ve)
			Views_result=views
	else:
		Views_result = int(float(views[:-1])*views_dict[views[-1]])

	return Views_result	

def fn(x, y):
	if x is None:
		x=[]
	elif y is None:
		y=[]
	else:
		return x+y


def AccessIndividual(geturl):	
	## accessing individual urls for thumbs up/ thumbs down/ tags/ comments(?)
	print("..............Getting individual url info..................")
	print(geturl)
	individual_url = requests.get(geturl)
	##  if access to individual urls success
	try:
		if individual_url.status_code == 200:
			print("..............individual url access success.................")
			individual_soup = BeautifulSoup(individual_url.text, 'html.parser')
			#print(individual_soup)

			## get views
			Vn=individual_soup.find(id="nb-views-number").get_text()
			Vn=Vn.replace(",","")
			Vn=int(Vn.strip())
			'''
			print(Vn)
			print(type(Vn))
			print(len(Vn))
'			'''
			## get final_tags
			tags = individual_soup.find_all("div","video-metadata video-tags-list ordered-label-list cropped")
			'''
			# getting tags as list
			final_tags=tags[0].get_text(",").split(',')
			final_tags.pop()  ## tags list of url
			'''
			## getting tags as text
			final_tags2=tags[0].get_text(",")  ## get as text
			final_tags2 = final_tags2[:-1]
			#print(final_tags)


			## get thumbs up/ thumbs down
			votes = individual_soup.find("span","vote-actions")
			#print(votes)
			thumbs=votes.get_text(",").split(',')
			#print(thumbs)

			if len(thumbs)==4:
				thumbs_up=ToNumberViews(thumbs[1])
				thumbs_down=ToNumberViews(thumbs[3])
			else:
				status=np.array(list(map(lambda x:len(x)>1,thumbs)))
				thumbs=np.array(thumbs)
				thumbs=thumbs[status]	
				thumbs_up=ToNumberViews(thumbs[0])
				thumbs_down=ToNumberViews(thumbs[1])

			#print(thumbs_up,thumbs_down)
			print("..............individual url access done.................")

			## get comment numbers
			# some posts don't have comments
			try:
				comment_n = individual_soup.find(id="tabComments_btn")
				#print("Comment_tag is: ",comment_n)
				comment_n = comment_n.get_text(",").split(",")
			
				if len(comment_n)==2:
					comment_number=int(comment_n[1])
				else:
					comment_number="NA"
			except AttributeError:
				comment_number = "NA"

		else:
			print("..............individual url access failed.................")
			thumbs_up = "NA"
			thumbs_down = "NA"
			final_tags = "NA"
			comment_number="NA"
	
	except Exception as ex_ind:
		print('Error: ',ex_ind,"=============")
		print(type(ex_ind))   # the exception instance
		print(ex_ind.args)
	
	return (
		{"Views":Vn,"Tags":final_tags2,"Thumbs_up":thumbs_up,"Thumbs_down":thumbs_down,"Comment_N":comment_number}
		)
	






def ScrapeAPage(url):

	try:
		resp = requests.get(url)
		if resp.status_code == 200:

			print("========= Access success....========= ")
			soup = BeautifulSoup(resp.text, 'html.parser')
			## prepare container for scraping data
			page = []
			div_test = soup.find_all("div","thumb-under")
			print("..............Executing..................")
			# Get all on first page
			for dvt in div_test:
				print("..............Getting url,title,time_length,author,views..................")
				# get url
				try:
					geturl = "https://www.xvideos.com"+dvt.find("a")['href']
					# get title
					title = dvt.find("a")['title']
					## prepare time author views
					info = dvt.find("p","metadata") 
					## get time
					time_length = info.find("span","duration").text
					# modify time 
					time_length = ToMins(time_length)

					## got author
					author = info.find("span","name").text
					print("..............Getting url,title,time_length,author  done##..................")
					## accessing individual urls for Views/thumbs up/ thumbs down/ tags/ comments(?)
					results={"Url":geturl,"Title":title,"Time":time_length,"Author":author}
					print(results)
					## adding element to existing dict
					results.update(AccessIndividual(geturl))
					print(results)
					page.append(results)
				except:
					pass
			end_time = time.time()
			print("=========....Scraping success....========= ")
			#print(page)
			return page
			time.sleep(1)
	
	except Exception as ex:
		print('Error: ',ex)
		print(page)
		print("========= Scraping failed....========= ")
		pass

# print(all_links[3])

#ScrapeAPage(all_links[0])


'''
## This is for scraping all pages using multiprocess  / multithreading crashes....
def Pages(pool_v,page):

	test_links = all_links[:page]
	start_time = time.time()
	with Pool(pool_v) as p:
		records=p.map(ScrapeAPage,test_links)
	print(len(records))
	
	p.terminate()
	p.join()
	end_time= time.time()
	print("Used up",format(end_time-start_time,".2E"),"secs...")
	#print(records)
	records = reduce(fn, records)  ## merging lists among lists
	print(len(records))

	xv_df=pd.DataFrame(records,columns=[
		"Url",
		"Title",
		"Time",
		"Author",
		"Views",
		"Tags",
		"Thumbs_up",
		"Thumbs_down",
		"Comment_N"
		])
	xv_df=xv_df.sort_values("Views",ascending=False)
	xv_df.to_csv('/Users/justin/Desktop/xv'+'_'+str(page)+'.csv',index=False,sep=",")
	
Pages(10,2)

'''

# for scraping ---
'''
print("How many pages do you want?")
howmany = int(input())
print("At what pace?")
pace = int(input())
Pages(pace,howmany)
'''



## output
import os
os.chdir("/Users/justin/Desktop/xvid_project/data")


for page_num, url in enumerate(all_links):

	print("Currently on page: ",page_num)
	page_info = ScrapeAPage(url)
	xv_df = pd.DataFrame(page_info,columns=[
			"Url",
			"Title",
			"Time",
			"Author",
			"Views",
			"Tags",
			"Thumbs_up",
			"Thumbs_down",
			"Comment_N"
			])

	# xv_df=xv_df.sort_values("Views",ascending=False)
	xv_df.to_csv('Page_'+str(page_num)+".csv",index=False,sep=",")
	

# page0 = ScrapeAPage(all_links[0])# 	
# page0 = pd.DataFrame(page0,columns=[
# 			"Url",
# 			"Title",
# 			"Time",
# 			"Author",
# 			"Views",
# 			"Tags",
# 			"Thumbs_up",
# 			"Thumbs_down",
# 			"Comment_N"
# 			])
# page0.to_csv("page0.csv",sep=",",index=False)


























