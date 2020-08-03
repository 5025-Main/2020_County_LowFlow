# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 12:30:18 2016

@author: alex.messina
"""

import time

from BeautifulSoup import BeautifulSoup

import numpy as np
import pandas as pd
import requests

import datetime as dt
import os

maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'
os.chdir('C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/Python_code/')

## Rain gauges indexed by rain gauge name
Rain_gauge_info = pd.DataFrame.from_csv(maindir+'Ancillary_files/Rain_gauge_info.csv')
## List of unique rain gauge names
Rain_gauge_names = Rain_gauge_info.index.unique()


######### UPDATE HERE ###################
#start_date, end_date = '2020-05-01', '2020-06-29' 
start_date, end_date = '2020-07-01', dt.date.today().strftime('%Y-%m-%d') ## for current day: dt.date.today().strftime('%Y-%m-%d')
time_bin  = '3600' #seconds. Daily=86400, Hourly=3600
#######################################


daterange = pd.date_range(start_date.replace('-',''),dt.datetime.now(),freq='D')


for Rain_gauge_name in Rain_gauge_names:
    print Rain_gauge_name
    RG_ID = str(Rain_gauge_info.ix[Rain_gauge_name]['rain_gauge_id'])
    print 'ID: '+ RG_ID
    RG_SERIAL = Rain_gauge_info.ix[Rain_gauge_name]['rain_gauge_serial']
    print 'SERIAL :'+RG_SERIAL
    RG_DEV_ID = str(Rain_gauge_info.ix[Rain_gauge_name]['rain_gauge_device_id'])
    print 'DEVICE ID: '+ RG_DEV_ID
    RG_DEV_SERIAL = Rain_gauge_info.ix[Rain_gauge_name]['rain_gauge_device_serial']
    print 'DEVICE SERIAL: '+ RG_DEV_SERIAL
    print '\n'

    site_df = pd.DataFrame()
    try:
        ## Verify rain gauge name
        url = 'https://sandiego.onerain.com/sensor.php?time_zone=US%2FPacific&site_id='+RG_ID+'&site='+RG_SERIAL+'&device_id='+RG_DEV_ID+'&device='+RG_DEV_SERIAL+'&bin='+time_bin+'&range=Custom+Range&legend=true&thresholds=true&refresh=off&show_raw=true&show_quality=true&data_start='+start_date+'+00%3A00%3A00&data_end='+end_date+'+23%3A59%3A59'
        
        s = requests.get(url).content
        
        soup = BeautifulSoup(s)
        
        try:
            print
            print 'Grabbing data for Rain gauge: '+Rain_gauge_name
            print '...from date range: '+str(daterange[0])+' to '+str(daterange[-1])
            try:
                ##enter web address of data
                #start_date = str(month.year)+'-'+str(month.month)+'-'+'01'
                #end_date = str(month.year)+'-'+str(month.month)+'-'+str(month.day)
                #start_date, end_date = str(date),str(date+ dt.timedelta(days=1))

                s = requests.get(url).content
                soup = BeautifulSoup(s)
                
                ## Check if this is rain increment data
                if len(soup.findAll('h1')) > 0:
                    if 'Rain Increment' in soup.findAll('h1')[0].text:        
                        print 'Rain Increment in Title...'
                        #print url
                        ## Get data from website
                        times, rain_vals = [], []
                        ## Get times
                        for h4_tag in soup.findAll('h4',{'class':'status-inline list-group-item-heading'}):
                            try:
                                datetime =  h4_tag.find('span', {'class':'text-nowrap'}).text
                                #print datetime
                                times.append(datetime)
                            except:
                                print 'Failed'
                                print h4_tag
                                print '\n'
                                pass
                        ## Get rain data
                        for h4_tag in soup.findAll('h4',{'class':'list-group-item-heading'}):
                            try:
                                rain_val =  h4_tag.text.split('&nbsp;')[0]
                                #print rain_val
                                rain_vals.append(float(rain_val))
                            except:
                                print 'Failed'
                                print h4_tag
                                print '\n'
                                pass
                        rain_data_df = pd.DataFrame({'Rain_in':rain_vals},index=pd.to_datetime(times)).sort_index()
                        rain_data_1hr = rain_data_df.resample('1H').sum().fillna(0.) 
                        rain_data_1D = rain_data_df.resample('D').sum()
                        
                        rain_data_1hr.to_csv(maindir+'Rain_data/'+Rain_gauge_name+'_hourly.csv')
                        rain_data_1D.to_csv(maindir+'Rain_data/'+Rain_gauge_name+'_daily.csv')
            except Exception as e:
                print (e)
                pass
        except Exception as e:
                print (e)
                pass
    except Exception as e:
                print (e)
                pass
            

        
#%%combine mutiple files


#Script expects the old files to be in a folder in the Raw data directory within the "0 - Rain Data". 
#Place newly downloaded rain data in a second folder in the same Raw data directory.
#The script will combine the files with the same names from each folder and output them to the raw data directory.

raindir = maindir+'Rain_data/'

old_rain_files = raindir+'June rain data/'
new_rain_files = raindir+'July rain data/'


for old_filename in os.listdir(old_rain_files):
    print old_filename
    rain_panda = pd.DataFrame()
    ## old file
    old_file = pd.read_csv(old_rain_files  + old_filename, index_col = 0)
    print(old_filename)
    ## new file
    new_filename = [f for f in os.listdir(new_rain_files) if f == old_filename][0]
    new_file = pd.read_csv(new_rain_files + new_filename, index_col = 0)
    print(new_filename)
    
    
    rain_panda = new_file.append(old_file)
    rain_panda['idx']=rain_panda.index
    rain_panda = rain_panda.drop_duplicates(subset='idx')
    rain_panda = rain_panda.sort_index()
#    print(rain_panda)
    rain_panda[['Rain_in']].to_csv(raindir+new_filename)

    
    
    

#%% Plot rain data
## Data from  https://sandiego.onerain.com/rain.php
raindir = maindir+'Rain_data/'
#for all gauges
rain_files = [f for f in os.listdir(maindir+'Rain_data/') if f.endswith('daily.csv')==True]
#for one gauge
#gauge_name = 'Flinn_Springs'
#rainfiles = [f for f in os.listdir(maindir+'Rain_data/') if f.endswith('daily.csv')==True]
#rainfiles = [f for f in os.listdir(maindir+'Rain_data/') if f.endswith('hourly.csv')==True]

fig, ax = plt.subplots(1,1,figsize=(12,8))

for rainfile in rain_files:
    print ('')
    print 'Precip file: '+rainfile
    rain = pd.read_csv(raindir+rainfile,index_col=0)
    rain.index = pd.to_datetime(rain.index)
    ## Resample to regular interval and fill non-data with zeros
    #rain = rain.resample('15Min').sum()
    

    ax.plot_date(rain.index, rain['Rain_in'],ls='steps-pre',marker='None',label=rainfile.split('_daily.csv')[0])
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m/%d/%Y'))
    
    
    #rain_1D.to_csv(daily_rain_files+'Daily-'+rainfile.replace('.xls','.csv'))
ax.set_ylabel('Rain in. (daily)')
ax.legend(ncol=4,fontsize=12)
plt.tight_layout()

