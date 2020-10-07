from selenium import webdriver
# headless browser
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# chrome_options = Options()
# chrome_options.add_argument("--headless")




def initiate(account,password):
	boa_url = "https://www.bankofamerica.com"

	## open bank of america website
	driver=webdriver.Chrome('./chromedriver')
	driver.get(boa_url)


	## enter account and password
	enter_account = driver.find_element_by_xpath('//*[(@id = "onlineId1")]')
	enter_password = driver.find_element_by_xpath('//*[(@id = "passcode1")]')
	login_button = driver.find_element_by_xpath('//*[(@id = "signIn")]')

	enter_account.send_keys(account)
	enter_password.send_keys(password)
	login_button.click()

	return driver

def wait(driver):
	## wait for  5 minutes
	driver.implicitly_wait(5)

def download(driver):	
	download = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "download-upper", " " ))]')
	download.click()

def customize_date(driver):
	customize = driver.find_element_by_xpath('//*[(@id = "cust-date")]')
	customize.click()

def pick_date(driver,start_date,end_date):
	#10/01/2020
	startdate = driver.find_element_by_xpath('//*[(@id = "start-date")]')
	enddate = driver.find_element_by_xpath('//*[(@id = "end-date")]')
	startdate.send_keys(start_date)
	enddate.send_keys(end_date)

def select_format(driver):
	select_format = driver.find_element_by_xpath('//*[(@id = "select_filetype")]')
	select_format.send_keys("Microsoft Excel Format")


def download_transaction(driver):
	download_transaction = driver.find_element_by_css_selector('form[name="transactionDownloadForm"] a > span')
	download_transaction.click()


def sequential_processing(driver,start_date,end_date):
	download(driver)
	wait(driver)
	customize_date(driver)
	wait(driver)
	pick_date(driver,start_date,end_date)
	wait(driver)
	select_format(driver)
	wait(driver)
	download_transaction(driver)


## Banking account
def banking(account,password,start_date,end_date):
	# initiate(account,password)
	driver = initiate(account,password)
	
	try:
		wait(driver)
		banking = driver.find_element_by_xpath('//li[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "AccountName", " " ))]//a')
		banking.click()
		sequential_processing(driver,start_date,end_date)

	except Exception as ex_ind:
		print('Error: ',ex_ind,"=============")
		print(type(ex_ind))   # the exception instance
		print(ex_ind.args)
		driver.close()

def savings(account,password,start_date,end_date,account_name):
	driver = initiate(account,password)
	## savings account
	try:
		wait(driver)
		#savings = driver.find_element_by_link_text("Advantage Savings - 1019")
		savings = driver.find_element_by_link_text(account_name)
		savings.click()
		sequential_processing(driver,start_date,end_date)

	except Exception as ex_ind:
		print('Error: ',ex_ind,"=============")
		print(type(ex_ind))   # the exception instance
		print(ex_ind.args)
		driver.close()

	## download file called stmt.csv


## credit card
def credit_card(account,password):
	driver = initiate(account,password)
	
	try:
		print("Got into try of credit card")
		wait(driver)
		print("got past wait")
		credit = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "AccountItemCreditCard", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "AccountName", " " ))]//a')
		credit.click()
		# click_download_btn = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "download-upper", " " ))]')
		wait(driver)
		driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "download-upper", " " ))]').click()
		wait(driver)
		select_format(driver)
		driver.find_element_by_css_selector('div#icon-legend-download a > span').click()
		wait(driver)
		time.sleep(10)
		print("Clicked download btn")

	except Exception as ex_ind:
		print('Error: ',ex_ind,"=============")
		print(type(ex_ind))   # the exception instance
		print(ex_ind.args)
		driver.close()
