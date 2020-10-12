import pandas as pd
import os
import re
import numpy as np

#########################################################################################


## input pandas dataframe you want to save, and specify which kine of bank account this is
def SaveFileInTransaction(file,typee,date,name_in_computer):

	transactions_dir = "/Users/"+name_in_computer+"/Desktop/boa/Transactions"

	if not os.path.exists(transactions_dir):
		os.mkdir(transactions_dir)
	else:
		os.chdir(transactions_dir)
		date = date.replace("/","-")
		file.to_csv(transactions_dir+"/"+date+"_"+typee+"_"+name_in_computer+".csv",sep=",")


## find the downloads file for a certain string eg. "Transactions", then iterate over them to get a pandas dataframe
def FindFile(findstring,name_in_computer):

	download_route = "/Users/"+name_in_computer+"/Downloads/"
	os.chdir(download_route)
	files_in_dir = os.listdir()
	check_dir = list(map(lambda x: re.search(findstring ,x)!= None,files_in_dir))
	download_index = np.where(check_dir)[0]
	#print(download_index)


	if len(download_index)>=1:

		myfile = pd.DataFrame()
		# concatenating all read in files
		for file in download_index:
			file_name = files_in_dir[file]
			#print(file_name)
			current_read_in_file = pd.read_csv(file_name)
			os.remove(file_name)  # remove the file from download
			myfile = pd.concat([myfile,current_read_in_file])
	
	else:
		myfile = "I can't find your Transactions file."

	return myfile




def TransactionsCredit(date,name_in_computer):

	## Searches the downloads file for Transaction.csv files then groups by payee, saved in the boa
	## transactions file. then removed from the downloads file, returns total money spent on crefit card
	start_date, end_date = date.split("_")
	myfile = FindFile("Transaction",name_in_computer)
	
	if type(myfile) == "str":
		print(myfile)
	else:
		
		# strip all amount > 0 
		myfile = myfile[myfile['Amount']<0]

		# filter by date
		myfile['Posted Date'] = pd.to_datetime(myfile['Posted Date'])
		time_interval = (myfile['Posted Date']>=start_date) & (myfile['Posted Date']<=end_date)
		myfile = myfile.loc[time_interval]

		#group by
		myfile_groupby_payee = myfile.groupby(['Payee'])['Amount'].sum().reset_index()
		myfile_groupby_payee.columns = ["Payee","Amount"]
		total_cost = myfile_groupby_payee['Amount'].sum()
		print(f'Your total expenses in credit card account is ${total_cost} USD.')
		SaveFileInTransaction(myfile_groupby_payee,"Credit",date,name_in_computer)

		return total_cost

#TransactionsCredit()




def TransactionsBanking(date,name_in_computer):
	## takes a statement file from downloads and sums up the money spent,saved in the boa
	## transactions file. then removed from the downloads file, returns total money spent
	download_route = "/Users/"+name_in_computer+"/Downloads/"

	with open(download_route+"stmt.csv") as reader:

		reader_list = reader.readlines()[6:] ## summary is from line 0 to 5

		data = []
		for line in reader_list:
			
			line = line.replace("\n","")
			line = line.replace('"',"")
			line = line.split(",")
			if line [0] == "Date":
				title = line
			else:
				data.append(line)

	statement_dict = {}

	for t in range(len(title)):

			statement_dict[title[t]] = list(map(lambda x:x[t] if len(x[t])>0 else "0",data))

	statement_dict = pd.DataFrame(statement_dict)
	statement_dict['Amount'] = statement_dict['Amount'].astype('float')

	amount_spent = statement_dict['Amount'].sum()
	running_balance = statement_dict['Running Bal.'][len(statement_dict['Running Bal.'])-1]

	print(f'Your total expenses in your Banking account is ${amount_spent} USD, while your running balance is ${running_balance}')

	SaveFileInTransaction(statement_dict,"BankingAccount",date,name_in_computer)
	os.remove(download_route+"stmt.csv")

	return amount_spent



#bank = TransactionsBanking()
#credit = TransactionsCredit()



## takes two amounts of money
def Payment(a,b,name_a,name_b):

	a_paid = abs(a)/2
	b_paid = abs(b)/2
	payment = a_paid - b_paid

	if payment > 0:
		msg = "{} needs to give {} {} dollars".format(name_b,name_a,abs(payment))
	else:
		msg = "{} needs to give {} {} dollars".format(name_a,name_b,abs(payment))

	return msg

