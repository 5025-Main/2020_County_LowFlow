# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:26:43 2020

@author: alex.messina
"""

import os
import pandas as pd
import pyodbc
import datetime as dt

##2015-2018

## Flow data
flow_data_df = pd.DataFrame(index=pd.date_range(dt.datetime(2015,5,1,0,0),dt.datetime(2018,9,30,23,55),freq='5Min'))
flow_datadir = 'P:/Projects-South/Environmental - Schaedler/5025-18-4055 COSD TO 55 Low Flow Data Mngmt/DATA/Flow totals-Postseason 2018/Compiled Level Flow Data 2015-2018/'
for f in [d for d in os.listdir(flow_datadir) if d.endswith('.csv')]:
    site_name = 'MS4-' +f.split('-Flow.csv')[0]
    print f

    df = pd.read_csv(flow_datadir + f, index_col=0)
    df['Datetime'] = df.index
    flow_col = site_name + '_Flow_gpm'
    ## add column to df
    flow_data_df.loc[:,flow_col] = df['Flow (gpm) CTRSC no stormflow']
#flow_data_df.to_csv('C:/Users/alex.messina/Desktop/Temporary_work_shit/County Weirs/'+'Flow data for MS4 sites 2015-2018.csv')   

## Flow data
flow_data_df2019 = pd.DataFrame(index=pd.date_range(dt.datetime(2019,5,1,0,0),dt.datetime(2019,9,15,23,55),freq='5Min'))
flow_datadir = 'P:/Projects-South/Environmental - Schaedler/5025-19-4063 COSD TO 63 Isotope and Geochem Sampling/5. Field Records/ANALYSIS/Flow/2019/'
for f in [d for d in os.listdir(flow_datadir) if d.endswith('.xlsx')]:
    site_name = 'MS4-' +f.split('-working draft.xlsx')[0]
    print f

    df = pd.read_excel(flow_datadir + f,sheetname=site_name.replace('MS4-','')+'-stormflow clipped', index_col=0)
    df['Datetime'] = df.index
    flow_col = site_name + '_Flow_gpm'
    ## add column to df
    flow_data_df2019.loc[:,flow_col] = df['Flow compound weir stormflow clipped (gpm)']
 
    


flow_data_df.append(flow_data_df2019).to_csv('C:/Users/alex.messina/Desktop/Temporary_work_shit/County Weirs/'+'Flow data for MS4 sites 2015-2019.csv')



#%%
## Add flow data to Access db


## Access database
dbpath = 'C:/Users/alex.messina/Desktop/FlowData.accdb'
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+dbpath+';')
crsr = conn.cursor()
table_name = "FLow_gpm"
crsr.fast_executemany = True

## Make field (column) for new data
crsr.execute( "ALTER TABLE %s ADD COLUMN [%s] FLOAT;"% (table_name,flow_col) )
conn.commit()



## update column values where Datetime Index row is same
#crsr.executemany("UPDATE %s SET [%s] = ? WHERE [Datetime] = ?"% (table_name,flow_col), df[['Flow (gpm)','Datetime']].itertuples(index=False))
for index,row in df[['Flow (gpm)']].itertuples():
    #print row
    crsr.execute("UPDATE %s SET [%s] = ? WHERE [Datetime] = ?"% (table_name,flow_col), (row,index) )
    conn.commit()

conn.close()
#%%






#pd.read_sql('select * from Flow_gpm',conn,index_col='Datetime')

# insert the rows from the DataFrame into the Access table   
#query = "INSERT INTO %s (Datetime, %s) VALUES (?)" % (table_name, flow_col)

#crsr.executemany("INSERT INTO %s ([Datetime], [%s]) VALUES (?,?);"% (table_name,flow_col), df[['Flow (gpm)']].itertuples())
for index,row in df[['Flow (gpm)']].itertuples():
    #print row
    crsr.execute("UPDATE %s SET [%s] = ? WHERE [Datetime] = ?"% (table_name,flow_col), (row,index) )




