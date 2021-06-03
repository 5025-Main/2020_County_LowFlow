# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:25:06 2021

@author: alex.messina
"""
import requests
import json
import pandas as pd
import datetime as dt
import time

today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)

# get_readings example
device_sn = "06-02192"
token = "Token {TOKEN}".format(TOKEN="5570f23feeb666615003051140cea73ccdb18639")
url = "https://zentracloud.com/api/v3/get_readings/"
headers = {'content-type': 'application/json', 'Authorization': token}
output_format = "df"

#startdate = '05-16-2019 00:00'
startdate = yesterday.strftime("%m-%d-%Y")
enddate = today.strftime("%m-%d-%Y")




params = {'device_sn': device_sn, 'output_format': output_format,'sort_by':'ascending','start_date':startdate,'end_date':enddate}

params = {'device_sn': device_sn, 'output_format': output_format,'per_page':2000,'sort_by':'ascending','start_date':startdate}

response = requests.get(url, params=params, headers=headers)
print (response)
if response.ok:
    content = json.loads(response.content)
    df = pd.read_json(content['data'], convert_dates=False, orient='split')
    print (df[['mrid','datetime','measurement','value','units']])
else:

    try:
        print ('waiting 65 sec....')
        time.sleep(35)
        print ('30 more sec....')
        time.sleep(27)
        print ('3')
        time.sleep(1)
        print ('2')
        time.sleep(1)
        print ('1')
        time.sleep(1)
        response = requests.get(url, params=params, headers=headers)
        print (response)
        if response.ok:
            content = json.loads(response.content)
            df = pd.read_json(content['data'], convert_dates=False, orient='split')
            print (df[['mrid','datetime','measurement','value','units']])
    except:
        print (response)
        
        

