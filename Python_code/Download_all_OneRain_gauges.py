# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:31:29 2020

@author: alex.messina
"""

## Download all the OneRain data
## Get Master Site List
rain_gauges_list = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/Rain_gauge_to_sites_list.csv',index_col=0)

## Download details for OneRain gauges
Rain_gauge_info = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/Rain_gauge_info.csv',index_col=0) # GitHub


for rain_gauge_name in rain_gauges_list:


## Get the rain gauge data from One Rain
print 'downloading data...'
Rain1D = get_OneRain_data(rain_gauge_name,start_date,end_date,Rain_gauge_info,time_bin='86400')

