# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:42:51 2020

@author: alex.messina
"""

## Download all sites from Zentra Cloud and put in folder. This will then get updated on GitHub and the Jupyter notebook can pull the data from git
import pandas as pd
from ZentraAPI import *
from pytz import timezone
import datetime as dt

if __name__ == "__main__":
    
    ## Format for UTC
    mytz = timezone('US/Pacific')
    start_time_loc = dt.datetime(2020,5,1,0,0)
    start_time_loc = mytz.normalize(mytz.localize(start_time_loc,is_dst=True))
    
    ## Get Master Site List
    site_list = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/MasterSiteList.csv')
    
    ## Loop through all sites
    for site_name in site_list['Site'][-1:]:
        print site_name
        
        try:
            ## Get existing data on GitHub to get last data point
            WL_existing = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv',index_col=0)
            # Last existing data point
            last_data_time = pd.to_datetime(WL_existing.index[-1])
            print 'Last data point in existing data at: '+last_data_time.strftime("%m/%d/%Y %H:%M")
            mytz = timezone('US/Pacific')
            last_data_time_loc = mytz.normalize(mytz.localize(last_data_time,is_dst=True))
                
            ## Call Zentra API to get data from last start time to current
            WL_new = getDeviceReadings(site_name, last_data_time_loc+ dt.timedelta(minutes=5))
            ## update with new data
            WL = WL_existing.append(WL_new)
        except:
            ## Call Zentra API to get data from last start time to current
            WL = getDeviceReadings(site_name,start_time_loc)
        
        ## Save raw data to csv
        maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'
        WL[['in Water Level',u'°F Water Temperature',u'mS/cm EC',u' Sensor Metadata',u'% Battery Percent','mV Battery Voltage','kPa Reference Pressure',u'\xb0F Logger Temperature']].to_csv(maindir+'Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv',encoding='utf-8')
