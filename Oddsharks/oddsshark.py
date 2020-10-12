import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from datetime import timedelta
import time

## dictionaries
month_name = {
    '01':'january',
    '02':'february',
    '03':'march',
    '04':'april',
    '05':'may',
    '06':'june',
    '07':'july',
    '08':'august',
    '09':'september',
    '10':'october',
    '11':'november',
    '12':'december'
}

Team_transform = {
'亞特蘭大老鷹':['atlanta','Hawks'],
'波士頓塞爾提克':['boston',"Celtics"],
'布魯克林籃網':['brooklyn','Nets'],
'夏洛特黃蜂':['charlotte','Hornets'],
'芝加哥公牛':['chicago','Bulls'],
'克里夫蘭騎士':['cleveland','Cavaliers'],
'達拉斯獨行俠':['dallas','Mavericks'],
'丹佛金塊':['denver','Nuggets'],
'底特律活塞':['detroit','Pistons'],
'金州勇士':['golden-state','Warriors'],
'休士頓火箭':['houston','Rockets'],
'印第安那溜馬':['indiana','Pacers'],
'洛杉磯快艇':['los-angeles','Clippers'],
'洛杉磯湖人':['los-angeles','Lakers'],
'曼斐斯灰熊':['memphis','Grizzlies'],
'邁阿密熱火':['miami','Heat'],
'密爾瓦基公鹿':['milwaukee','Bucks'],
'明尼蘇達灰狼':['minnesota','Timberwolves'],
'紐奧良鵜鶘':['new-orleans','Pelicans'],
'紐約尼克':['new-york','Knicks'],
'奧克拉荷馬雷霆':['oklahoma-city','Thunder'],
'奧蘭多魔術':['orlando','Magic'],
'費城76人':['philadelphia','76ers'],
'鳳凰城太陽':['phoenix','Suns'],
'波特蘭拓荒者':['portland','Blazers'],
'沙加緬度國王':['sacramento','Kings'],
'聖安東尼奧馬刺':['san-antonio','Spurs'],
'多倫多暴龍':['toronto','Raptors'],
'華盛頓巫師':['washington','Wizards'],
'猶他爵士':['utah','Jazz']
}

## first function, input game_url in oddsharks

def Get_Website_Info(url):
    
    response = requests.get(url,timeout=None)
    
    if response.status_code ==404:
        return "Wrong"
    
    
    elif response.status_code ==200:
        response= BeautifulSoup(response.text, 'html.parser')
        script = response.select('script')

        ## get header
        header=script[0].contents[0]
        final_header = header.string
        header_dict = json.loads(final_header)

        ## get info
        content=script[3].contents[0]
        final_content = content.string
        final_content = json.loads(final_content) 
        final_info = final_content['oddsshark_gamecenter']

        return [header_dict,final_info]

## Process Head to Head and Team Records

def Process_stats(infoo,inputcategory):

    desired_info = infoo[inputcategory]
    
    output = dict()
    
    category = desired_info['title']
    
    for di in desired_info['tabs']:
        title = di['title']
        data = di['data']
        for dt in data:
            label = category+"_"+title+"_"+dt['label']
            away_team_stat = dt['away']['value']
            home_team_stat = dt['home']['value']
            output[label]=[away_team_stat,home_team_stat]
        
    return output


## final version 
## use two functions  Get_Website_Info ; Process_stats
### final version


## main crawler
def Oddshark_crawler(url):
    
    if Get_Website_Info(url)=="Wrong":
        return "Exit"
    else:
        
        header = Get_Website_Info(url)[0]
        info = Get_Website_Info(url)[1]

        ## header_dict
        header_dict = {
        'status':['away','home'],
        'Team':[header['awayTeam']['name'],header['homeTeam']['name']],
        'Date':[header['startDate'],header['startDate']]
        }

        HeadtoHead = Process_stats(info,'headToHead')
        teamRecords = Process_stats(info,'teamRecords')
        HeadtoHead.update(teamRecords)

        final_dict = {}
        final_dict.update(header_dict)
        final_dict.update(HeadtoHead)
        final_dict.update(teamRecords)

        # df_stat
        df_stat=pd.DataFrame.from_dict(final_dict)

        ## edgeFinder 

        edgefinder = info['edgeFinder']['data']
        #edgefinder.keys()  # dict_keys(['overall', 'scoring', 'shooting', 'rebounds', 'other'])

        edge_category = ['overall', 'scoring', 'shooting', 'rebounds', 'other']
        team_category = ['offensive', 'defensive', 'relative_offensive', 'relative_defensive']

        tc_dict = dict()

        for ec in edge_category:

            for tc in team_category:

                away_tc = edgefinder[ec]['away'][tc]
                home_tc = edgefinder[ec]['home'][tc]


                if home_tc.keys() == away_tc.keys():

                    for tc_keys in home_tc.keys():

                        home_tc_keys = float(home_tc[tc_keys]['stat'])
                        away_tc_keys = float(away_tc[tc_keys]['stat'])

                        tc_dict[ec+"_"+tc+"_"+tc_keys] = [away_tc_keys,home_tc_keys]

        tc_df =pd.DataFrame.from_dict(tc_dict)
        tc_df['status'] = ['away','home']

        ## merge two dataframes ; outerjoin
        final_dataframe = pd.merge(df_stat,tc_df,on="status",how="outer")

        ## return results
        return final_dataframe


## Match with Team
def Match_With_Team(Team):

  if Team in Team_transform.keys():

    Team_code = Team_transform[Team][0]
    English_Team_name = Team_transform[Team][1]
  
  else:

    Team_code = "Outlier"
    English_Team_name = "Outlier"

  return [Team_code,English_Team_name]


#usa_gameday
def change_usa_day(x):
    ts = datetime.strptime(x,'%Y-%m-%d')
    ts_usa = str(ts - timedelta(days=1)).split(" ")[0]
    return ts_usa



## data processing
def Process(df):
	df.drop(df[df["GameID"]=="Nothing"].index,inplace=True)
	df['隊伍代碼']  = df['隊伍'].apply(lambda x: Match_With_Team(x)[0])
	df['英文隊伍名稱']  = df['隊伍'].apply(lambda x:Match_With_Team(x)[1])
	## data processing
	df['GameID'] = df['GameID'].apply(lambda x: str(x))
	df['GameDay'] = df['GameID'].apply(lambda x: x[:4]+"-"+x[4:6]+"-"+x[6:8]) 
	df['USA_GameDay'] = df['GameDay'].apply(lambda x: change_usa_day(x))	

	return df


## based on betting webiste data
def Geturl(df):
    
    result_url = []
    oddsharks_header=  "https://www.oddsshark.com/nba/"  
    unique_ids = df['GameID'].unique()
    
    
    for uids in unique_ids:
        
        #print(uids)
        ## get the two teams
        current_id_data = df[df['GameID']==uids]
        teams = current_id_data['隊伍代碼'].values
        team1 = teams[0]
        team2 = teams[1]
        
        ## url_day_format
        current_day=current_id_data['USA_GameDay'].values[0]
        day = current_day.split("-")
        year = day[0]
        #print(year)
        month = day[1]
        #print(month)
        d = day[2]
        if d in ["01","02","03","04","05","06","07","08","09"]:
        	d = d.strip("0")
        #print(d)
        #print(month_name[month])
        url_day_format = month_name[month]+"-"+d+"-"+year+"-"
        
        result = oddsharks_header+team1+"-"+team2+"-"+"odds-"+url_day_format
        #print(result)
        result_url.append(result)
        
    return result_url


def Guess(data):
    
    final_data = pd.DataFrame()
    
    urls = Geturl(data)
    indexes = range(891310,891310+len(urls)*5,5)
    
    progress = 0

    if len(urls) == len(indexes):
        
        for tick in range(len(urls)):
            
            url = urls[tick]
            index = indexes[tick]
            ## try +- 20
            
            ## try the original url first
            if requests.get(url+str(index)).status_code == 200:
            	print("This url is correct")
            	confirmed_url = url+str(index)
            
            else:
            	print("Checking alternatives")
            	suspicious_indexes = [index+5,index-5,index+10,index-10,index+15,index-15,index+20,index-20]

            	for si in suspicious_indexes:    
	           
	                test_url = url + str(si)
	            
	                response = requests.get(test_url)

	                if response.status_code ==200:
	                    confirmed_url = test_url
	                    break
                            
            matched_df = Oddshark_crawler(confirmed_url)
            final_data = pd.concat([matched_df,final_data])
            progress +=1
            print("Current Progress: ",round(progress/len(urls)*100,1),"%",";","index: ",progress)
            if progress%10 ==0:
            	time.sleep(1)
            #print(final_data)


    
    return final_data
            


## Main process

'''
data_2018 = pd.read_csv('/Users/justin/Desktop/data2018.csv')
data_2018 = Process(data_2018)

Guess_data_2018 = Guess(data_2018)
Guess_data_2018.to_csv('/Users/justin/Desktop/Guess_data_2018.csv',index=False,sep=",")


urls=Geturl(data_2018)
r=range(891310,891310+len(urls)*5,5)
urlss=[]
for url in range(len(urls)):
	urlss.append(urls[url]+str(r[url]))
#print(urlss)
test = urlss[11]
print(Oddshark_crawler(urlss[11]))
print(Oddshark_crawler(urlss[12]))
print(Oddshark_crawler(urlss[13]))

'''

#accessible=list(map(lambda x:requests.get(x).status_code==200,test))
'''
for t in test:
	if requests.get(t).status_code==200:
		print(True)
	else:
		print(False)
'''

## The guess function only applies for 2018 only now
#Guess_data_2018 = Guess(data_2018)
#Guess_data_2018.to_csv('/Users/justin/Desktop/Guess_data_2018.csv',index=False,sep=",")

#https://www.oddsshark.com/nba/phoenix-denver-odds-january-3-2018-891445 ## correct
#https://www.oddsshark.com/nba/phoenix-denver-odds-january-03-2018-891445






