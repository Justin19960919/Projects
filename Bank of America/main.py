from download import wait, download, customize_date, pick_date, select_format, download_transaction, sequential_processing, banking, savings, credit_card

from merge import SaveFileInTransaction,FindFile,TransactionsCredit,TransactionsBanking,Payment

import pandas as pd
import os
import re
import numpy as np

from selenium import webdriver
# headless browser
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup as bs
# from selenium.webdriver.supportui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


def main():

	## download file start
	## input account and password
	print("You have activated the Bank Of America download script")
	account = input("Please enter your account name: ")
	password = input("Please enter your password: ")
	## initiate selenium
	selection = int(input("Please select which account you want to access:\n1. banking\n2.savings\n3.credit card\n4.All\n"))

	## user input date
	start_date = input("Please input start date in format (mm/dd/yyyy): ")
	end_date = input("Please input start date in format (mm/dd/yyyy): ")
	date = start_date+"_"+end_date
	
	#  User input username
	username = input("Please type in your username in computer: ")

	if selection == 1:
		banking(account,password,start_date,end_date)
		print("During {} to {}; ".format(start_date,end_date))
		banking_cost = TransactionsBanking(date,username)
	
	elif selection == 2:
		account_name = input("Please type in your account name: (listed in BOA website)")
		print("During {} to {}; ".format(start_date,end_date))
		savings(start_date,end_date,account_name)
	
	elif selection == 3:
		credit_card(account,password)
		print("During {} to {}; ".format(start_date,end_date))
		credit_card_cost = TransactionsCredit(date,username)
		## add function to select only transactions in the required timeframe
	elif selection ==4:
		print("During {} to {}; ".format(start_date,end_date))
		banking(account,password,start_date,end_date)
		banking_cost = TransactionsBanking(date,username)
		credit_card(account,password)
		credit_card_cost = TransactionsCredit(date,username)
		print(f'Total Costs: ${banking_cost+credit_card_cost} USD.')


if __name__ == "__main__":
	main()
