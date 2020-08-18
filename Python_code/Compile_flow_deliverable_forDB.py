# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:14:57 2020

@author: alex.messina
"""

import os
import pandas as pd
import pyodbc
import datetime as dt


## Flow data
flow_data_df = pd.DataFrame(index=pd.date_range(dt.datetime(2020,5,1,0,0),dt.datetime(2019,9,15,23,55),freq='5Min'))

flow_datadir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/Flow_Output_Excel_files/'

for f in [d for d in os.listdir(flow_datadir) if d.endswith('.xlsx')]:
    site_name = 'MS4-' +f.split('-working draft.xlsx')[0]
    print f

    df = pd.read_excel(flow_datadir + f,sheetname=site_name.replace('MS4-','')+'-stormflow clipped', index_col=0)
    df['Datetime'] = df.index
    flow_col = site_name + '_Flow_gpm'
    ## add column to df
    flow_data_df.loc[:,flow_col] = df['Flow compound weir stormflow clipped (gpm)']
#%%
flow_data_df.to_csv('C:/Users/alex.messina/Desktop/Temporary_work_shit/County Weirs/'+'Flow data for MS4 sites 2015-2019 Wood.csv') 