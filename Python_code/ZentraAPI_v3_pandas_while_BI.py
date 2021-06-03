f# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:25:06 2021

@author: alex.messina
"""
import requests
import json
import pandas as pd
import datetime as dt
import time

startTime = dt.datetime.now()

### DEVICE
device_sn = "06-02238"


### START/END DATES
today = dt.datetime.now()
days_ago = today - dt.timedelta(days=2) ## get data from past 12 days
startdate = days_ago.strftime("%m-%d-%Y")
enddate = today.strftime("%m-%d-%Y")

# or hardcode start/end
#startdate = '05-5-2021'
#enddate = '05-7-2021'

### API PARAMS
#token = "Token {TOKEN}".format(TOKEN="5570f23feeb666615003051140cea73ccdb18639") ## Wood API token
token = "Token {TOKEN}".format(TOKEN="0e599fae024923f65b51a73cbb19ee94ae729444") ## KLI API token
url = "https://zentracloud.com/api/v3/get_readings/"
headers = {'content-type': 'application/json', 'Authorization': token}
output_format = "df"
perpage = 2000
params = {'device_sn': device_sn, 'output_format': output_format,'per_page':2000,'sort_by':'ascending','start_date':startdate,'end_date':enddate}

## GET DATA FUNCTION
def get_zentra_df(url, params, headers, retries=3):
    ## Initial request
    response = requests.get(url, params=params, headers=headers)
    ## If good response [200] then parse data and return the df
    if response.ok:
        print ('Succesful response.')
        content = json.loads(response.content)
        if content['pagination']['page_num_readings']>0:
            df = pd.read_json(content['data'], convert_dates=False, orient='split')
            print (df[['datetime', 'mrid', 'measurement','value', 'units']].head())
            print (df[['datetime', 'mrid', 'measurement','value', 'units']].tail())
        else:
            df = pd.DataFrame()
    ## If no good response [429], need to wait and try again
    else:
        success = False #False til good response
        fails = 1 #set fails to 1 for first loop
        fail_count = retries # 3 retries by default
        while fails <= fail_count and  success==False:
            print ('Failed '+str(fails)+' time(s). '+str(response))
            print ('Waiting to retry...')
            time.sleep(65)
            print ('trying....')
            response = requests.get(url, params=params, headers=headers)
            ## If good response after waiting 65 sec...
            if response.ok:
                success = True
                content = json.loads(response.content)
                if content['pagination']['page_num_readings']>0:
                    df = pd.read_json(content['data'], convert_dates=False, orient='split')
                    print (df[['datetime', 'mrid', 'measurement','value', 'units']].head())
                    print (df[['datetime', 'mrid', 'measurement','value', 'units']].tail())
                else:
                    df = pd.DataFrame()
            else:
                print ('Failed '+str(response))
                pass
            fails +=1 ## count fails up 1 every loop
        ## If 3 tries are all fails raise error
        if fails > fail_count and success==False:
            raise Exception(response)
            print ('Failed after '+str(retries)+' response: '+str(response))
        if success == True:
            print ('Successful after '+str(fails)+' tries')
            pass
    return df, content



## Empty dataframe for data
dat = pd.DataFrame()

## FIRST PAGE OF DATA
df, content = get_zentra_df(url, params=params, headers=headers)
dat = dat.append(df)

## NEXT PAGE(S)
length_data = content['pagination']['page_num_readings']
next_url = content['pagination']['next_url']
## loop until a page returns with no data
while length_data > 0:
    next_df, next_content = get_zentra_df(next_url, params, headers, retries=3)
    if next_content['pagination']['page_num_readings'] > 0: ## if it actually returns data, if not df is empty
        dat = dat.append(next_df)
        ## update length data and next_url with this page's values
        length_data = next_content['pagination']['page_num_readings']
        next_url = next_content['pagination']['next_url']
    else:
        length_data = 0
        
dat = dat.replace(2579.29, np.nan)
dat['datetime'] = pd.to_datetime(dat['datetime'])

#Python 3: 
print ('Script downloaded data in:')
print(dt.datetime.now() - startTime)

#for name in dat['measurement'].unique():
#    print (name)
#    print (dat[dat['measurement']=='Water Level']['value'].max())
    

for i in range(1,6):
    print (i)
    try:
        port = dat[ (dat['measurement']=='Water Level') & (dat['port_num']== i ) ] [['datetime', 'mrid', 'measurement','value', 'units']]
        plt.plot_date(port['datetime'],port['value'],ls='-',marker='None',label='port '+str(i)) 
        plt.xlim(port['datetime'].min(), port['datetime'].max())
    except:
        print ('Port no worky')
        pass


