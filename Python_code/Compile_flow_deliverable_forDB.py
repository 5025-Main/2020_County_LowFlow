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
flow_data_df.to_csv(flow_datadir + '2020_Flow_compiled.csv') 

#%%
df = pd.DataFrame(columns=['DateTime','Flow_gpm','Latitude','Longitude'])

site_list = pd.read_csv('C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/Ancillary_files/MasterSiteList.csv',index_col = 0)

for col in flow_data_df.columns:
    site = col.split('_Flow_gpm')[0].replace('MS4-','')
    print site
    lat, lon = site_list.ix[site][['Latitude','Longitude']].values
    ## Get flow data for site
    site_df = pd.DataFrame( flow_data_df[col] )
    site_df.columns = ['Flow_gpm'] #rename to generic Flow_gpm
    site_df['DateTime'] = site_df.index
    
    ## Add lat/lon
    site_df['Latitude'] = lat
    site_df['Longitude'] = lon
    ## Add SiteID as a column
    site_df['SiteID'] = 'MS4-'+site
    ## And make it the index
    site_df = site_df.set_index(site_df['SiteID'])
    
    df = df.append(site_df[['DateTime','Flow_gpm','Latitude','Longitude']])

df.to_csv(flow_datadir + '2020_Flow_compiled_longform.csv')
#%%


## Temp data
temp_data_df = pd.DataFrame(index=pd.date_range(dt.datetime(2020,5,1,0,0),dt.datetime(2019,9,15,23,55),freq='5Min'))

datadir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/Flow_Output_Excel_files/'

for f in [d for d in os.listdir(datadir) if d.endswith('.xlsx')]:
    site_name = 'MS4-' +f.split('-working draft.xlsx')[0]
    print f

    df = pd.read_excel(datadir + f,sheetname=site_name.replace('MS4-','')+'-stormflow clipped', index_col=0)
    df['Datetime'] = df.index
    temp_col = site_name + '_Temp_F'
    ## add column to df
    temp_data_df.loc[:,temp_col] = df[u'°F Water Temperature']
#%%
temp_data_df.to_csv(datadir + '2020_Temp_compiled.csv') 


#%%


## Conductivity data
cond_data_df = pd.DataFrame(index=pd.date_range(dt.datetime(2020,5,1,0,0),dt.datetime(2019,9,15,23,55),freq='5Min'))

datadir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/Flow_Output_Excel_files/'

for f in [d for d in os.listdir(datadir) if d.endswith('.xlsx')]:
    site_name = 'MS4-' +f.split('-working draft.xlsx')[0]
    print f

    df = pd.read_excel(datadir + f,sheetname=site_name.replace('MS4-','')+'-stormflow clipped', index_col=0)
    df['Datetime'] = df.index
    cond_col = site_name + '_Cond_uScm'
    ## add column to df
    cond_data_df.loc[:,cond_col] = df[u'uS/cm EC']
#%%
cond_data_df.to_csv(datadir + '2020_Cond_compiled.csv') 







