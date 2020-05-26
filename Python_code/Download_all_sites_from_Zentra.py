# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:42:51 2020

@author: alex.messina
"""

## Download all sites from Zentra Cloud and put in folder. This will then get updated on GitHub and the Jupyter notebook can pull the data from git
import pandas as pd
from ZentraAPI import *
from pytz import timezone


if __name__ == "__main__":
    
    ## Format for UTC
    mytz = timezone('US/Pacific')
    start_time_loc = dt.datetime(2020,5,1,0,0)
    start_time_loc = mytz.normalize(mytz.localize(start_time_loc,is_dst=True))
    
    ## Device info for Meter units
    device_df = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/Meter_SN_pwd_list.csv',index_col=0)
    
    ## Get Master Site List
    site_list = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/MasterSiteList.csv')
    
    ## Loop through all sites
    for site_name in site_list['Site'].values[7:]:
        print site_name
    
        ## Call Zentra API to get data from start time to current
        
        WL = getDeviceReadings(site_name, start_time_loc,device_df)
        
        ## Save raw data to csv
        maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'
        WL.to_csv(maindir+'Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv',encoding='utf-8')