# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:44:03 2021

@author: alex.messina
"""

import requests
import json
import pandas as pd
import datetime as dt
import time

startTime = dt.datetime.now()

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
                    print ('Device data: ')
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

### DEVICE
site_device_dict = {'CAR-059':('06-02192',3),
                  'CAR-070':('06-02245',3),
                  'CAR-070E':('06-02351',3),
                  'CAR-072':('06-02301',3),
                  'CAR-072C':('06-02127',3),
                  'CAR-072Q':('06-02190',3),
                  'CAR-072R':('06-02298',3),
                  'SDG-072':('06-02290',3),
                  'SDG-072F':('06-02299',3),
                  'SDG-084':('06-02207',3),
                  'SDG-084J':('06-02230',3),
                  'SDG-085':('06-02293',3),
                  'SDG-085G':('06-01630',3),
                  'SDG-085M':('06-02235',3),
                  'SDR-036':('06-02199',3),
                  'SDR-041':('06-02246',3),
                  'SDR-064':('06-02212',3),
                  'SDR-064A':('06-02229',3),
                  'SDR-098':('06-02203',3),
                  'SDR-127':('06-02204',3),
                  'SDR-130':('06-02198',3),
                  'SDR-203A':('06-02255',2),
                  'SDR-204A':('06-02255',5),
                  'SDR-768':('06-02193',3),
                  'SLR-045':('06-02227',3),
                  'SLR-045A':('06-02210',2),
                  'SLR-045B':('06-02210',5),
                  'SLR-156':('06-02211',3),
                  'SLR-160':('06-02337',3),
                  'SLR-160A':('06-02219',3),
                  'SWT-030':('06-02256',3),
                  'SWT-049':('06-02285',3)}

                    
device_site_dict= {'06-02192':(['CAR-059'],3),
                '06-02245':(['CAR-070'],3),
                '06-02351':(['CAR-070E'],3),
                '06-02301':(['CAR-072'],3),
                '06-02127':(['CAR-072C'],3),
                '06-02190':(['CAR-072Q'],3),
                '06-02298':(['CAR-072R'],3),
                '06-02290':(['SDG-072'],3),
                '06-02299':(['SDG-072F'],3),
                '06-02207':(['SDG-084'],3),
                '06-02230':(['SDG-084J'],3),
                '06-02293':(['SDG-085'],3),
                '06-01630':(['SDG-085G'],3),
                '06-02235':(['SDG-085M'],3),
                '06-02199':(['SDR-036'],3),
                '06-02246':(['SDR-041'],3),
                '06-02212':(['SDR-064'],3),
                '06-02229':(['SDR-064A'],3),
                '06-02203':(['SDR-098'],3),
                '06-02204':(['SDR-127'],3),
                '06-02198':(['SDR-130'],3),
                '06-02255':(['SDR-203A','SDR-204A'],[2,5]),
                '06-02193':(['SDR-768'],3),
                '06-02227':(['SLR-045'],3),
                '06-02210':(['SLR-045A','SLR-045B'],[2,5]),
                '06-02211':(['SLR-156'],3),
                '06-02337':(['SLR-160'],3),
                '06-02219':(['SLR-160A'],3),
                '06-02256':(['SWT-030'],3),
                '06-02285':(['SWT-049'],3)}

### START/END DATES
today = dt.datetime.now()
days_ago = today - dt.timedelta(days=2) ## get data from past 12 days
startdate = days_ago.strftime("%m-%d-%Y")
enddate = today.strftime("%m-%d-%Y")

# or hardcode start/end
#startdate = '05-5-2021'
#enddate = '05-13-2021'

## Empty dataframe for data
level_dat = pd.DataFrame(index=pd.date_range(dt.datetime(2021,5,1,0,0),dt.datetime(2021,9,16,0,0),freq='5Min'))
temp_dat = pd.DataFrame(index=pd.date_range(dt.datetime(2021,5,1,0,0),dt.datetime(2021,9,16,0,0),freq='5Min'))
cond_dat = pd.DataFrame(index=pd.date_range(dt.datetime(2021,5,1,0,0),dt.datetime(2021,9,16,0,0),freq='5Min'))
## iterate over loggers, can get 60 loggers in 1 min from API or else throttled and have to wait 1min
for device_sn, (site_s, port_s) in device_site_dict.items():
    print()
    print ('Device: '+device_sn)
    
    ### API PARAMS
    token = "Token {TOKEN}".format(TOKEN="5570f23feeb666615003051140cea73ccdb18639")
    url = "https://zentracloud.com/api/v3/get_readings/"
    headers = {'content-type': 'application/json', 'Authorization': token}
    output_format = "df"
    perpage = 2000
    params = {'device_sn': device_sn, 'output_format': output_format,'per_page':2000,'sort_by':'ascending','start_date':startdate,'end_date':enddate}

    ## FIRST PAGE OF DATA
    df, content = get_zentra_df(url, params=params, headers=headers)
    df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)
    df.index = df['datetime']
    
    ## For each logger, if multiple sites then iterate over sites
    for site in site_s:
        port_num = site_device_dict[site][1]
        print ('Saving data for...')
        print (site, port_num)
        
        site_data = df[df['port_num']==port_num]
        
        site_level_data = site_data[site_data['measurement']=='Water Level']      [['datetime','mrid', 'measurement','value', 'units']]
        site_temp_data = site_data[site_data['measurement']=='Water Temperature'] [['datetime','mrid', 'measurement','value', 'units']]
        site_cond_data = site_data[site_data['measurement']=='EC']                [['datetime','mrid', 'measurement','value', 'units']]
    
        level_dat[site+'_level_in'] = site_level_data.drop_duplicates(subset=['datetime']).dropna(how='all')['value']
        temp_dat[site+'_temp_F'] = site_temp_data.drop_duplicates(subset=['datetime']).dropna(how='all')['value']
        cond_dat[site+'_cond_mScm'] = site_cond_data.drop_duplicates(subset=['datetime']).dropna(how='all')['value']
    
    
#Python 3: 
print ('Script downloaded data in:')
print(dt.datetime.now() - startTime)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    