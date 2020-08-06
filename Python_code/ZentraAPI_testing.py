# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:27:30 2020
@author: alex.messina
"""
import pandas as pd
import datetime as dt
import numpy as np
from pytz import timezone
import json
import urllib2
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'#+'test/'
# Format for UTC
mytz = timezone('US/Pacific')
start_time_loc = dt.datetime(2020,5,1,0,0)
start_time_loc = mytz.normalize(mytz.localize(start_time_loc,is_dst=True))
## Get Master Site List
site_list = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/MasterSiteList.csv')
## Just one site
site_list =  site_list[site_list['Site'] == 'SDG-287'] ###########

#site_list = site_list[~site_list['Site'].isin(['SLR-095','SDG-084','SDR-098','SDG-085G','SLR-045'])]

## Loop through all sites
for site_name in site_list['Site']:
    print
    print site_name
    try:
        ## Get existing data on GitHub to get last data point
        print 'Get existing data from '+'https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv'
        WL_existing = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv',index_col=0,encoding='utf-8')
        # Last existing data point
        last_data_time = pd.to_datetime(WL_existing.index[-1])
        print 'Last data point in existing data: '+last_data_time.strftime("%m/%d/%Y %H:%M")
        mytz = timezone('US/Pacific')
        last_data_time_loc = mytz.normalize(mytz.localize(last_data_time,is_dst=True))  
    except:        
        ## if no existing data set, just get data from May 1
        WL_existing = pd.DataFrame()
        last_data_time_loc = start_time_loc - dt.timedelta(minutes=5)
    ## Start downloading 5min after last data point 
    last_data_time_loc = last_data_time_loc + dt.timedelta(minutes=5)
    print 'Last data point in existing data at LOCAL: '+last_data_time_loc.strftime("%m/%d/%Y %H:%M")
    ## Call Zentra API to get data from last start time to current
    print 'Downloading data from Zentra API for site: ' + site_name
    print ' starting at '+last_data_time_loc.strftime("%m/%d/%Y %H:%M")
    ## API log in credentials
    user = "alex.messina@woodplc.com"
    user_password = "Mactec101"
    ## Device data on Serial number, password, and Port that probe is plugged into
    ## Device info for Meter units - stored on GitHub
    device_df = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Ancillary_files/Meter_SN_pwd_list.csv',index_col=0)
    logger_port = device_df.ix[site_name]['Port']
    device_serial_number = device_df.ix[site_name]['Serial Number']
    device_password = device_df.ix[site_name]['Password']
    ## API token parameters
    ip,key_name,token= "zentracloud.com",'AlexMessina','1a45a3456373971b5d1120ab9a9953e731f13402'
    ## Format start time
    mytz = timezone('US/Pacific')
    start_time_utc = last_data_time_loc.astimezone(timezone('UTC'))
    start_time  = int((start_time_utc-dt.datetime(1970,1,1,0,0,tzinfo=timezone('UTC'))).total_seconds())
    ## Construct url for API call
    print 'Downloading data from Zentra API.....please wait....'
    url = 'https://' + ip + '/api/v1/readings'+ '?' + "sn=" + device_serial_number+ '&' + "start_time=" + '%s'%start_time
    ## Request data from API
    request = urllib2.Request(url)
    request.add_header('Authorization','token %s' % token)
    request.add_header('Content-Type','application/json')
    ## Get response data
    response = urllib2.urlopen(request)
    readings_str = response.read()
    readings_json = json.loads(readings_str)
    # Readings are now contained in the 'readings_json' Python dictionary
    ## Data is read from JSON object using the zentra_json_parser defined above
#    with open(maindir+'logger.json', 'w') as outfile:
#        json.dump(readings_json, outfile)
    print 'Formatting data....please wait...'    
    json_obj = readings_json ## save original json obj
    ## Start with blank dataframe for results
    results_df = pd.DataFrame()
    ## Test first row to get the Port Number
    sensors = pd.DataFrame(json_obj['device']['timeseries'][0]['configuration']['sensors'])
    number_of_sensors = len(sensors[sensors['port'].isin([7,8])==False])
    for row in json_obj['device']['timeseries'][0]['configuration']['values']:
        #print row
        ## Row values are:
        ## 0 timestamp in UTC
        ## 1 mrid?
        ## 2 ??
        ## 3 - 5 ports (I think these change as ports are added)
        ## 6 battery percent, battery voltage
        ## 7 reference pressure, logger temperature
        ## Change UTC to local time
        utc_time = dt.datetime.utcfromtimestamp(row[0]).replace(tzinfo=timezone('UTC'))
        loc_time = utc_time.astimezone(timezone('US/Pacific')).replace(tzinfo=None)
        loc_time = pd.to_datetime(loc_time)
        #print 'Local time of reading: '+loc_time.strftime("%m/%d/%Y %H:%M")
        ## Extract measurement data using the defined port number (+1)
        try:
            site_sensor_position = 0
            if site_name in ['SLR-045B','SDG-287']:#,'SLR-095']:
                #print 'Sensor for '+site_name+' is in second plug position'
                site_sensor_position+=1
            if site_name in ['SDR-204A']:
                #print 'Sensor for '+site_name+' is in second plug position'
                site_sensor_position+=2  
                
            water_level_data = filter(lambda x: x[0]['description']=='Water Level', row[3:])[site_sensor_position] 
            meas_df = pd.DataFrame(water_level_data)
            ## Construct headers using units and parameter name
            meas_df.index =   meas_df['units'].str.strip(' ')+' '+meas_df['description']
            ## Transpose rows to column headers
            meas_df = meas_df.T
            meas_dict = dict(meas_df.ix['value'])
        except:
            raise
            print 'No Water Level data in description'
            meas_dict = {u' Sensor Metadata': np.nan, u'in Water Level':  np.nan, u'mS/cm EC':  np.nan, u'\xb0F Water Temperature':  np.nan}
        ## Extract battery level data
        battery_data = filter(lambda x: x[0]['description']=='Battery Percent',row[3:])[0]
        batt_df = pd.DataFrame(battery_data)
        batt_df.index =   batt_df['units'].str.strip(' ')+' '+batt_df['description']
        batt_df = batt_df.T
        batt_dict = dict(batt_df.ix['value'])
        ## Extract logger baro/temp data
        baro_data = filter(lambda x: x[0]['description']=='Reference Pressure',row[3:])[0]
        baro_df = pd.DataFrame(baro_data)
        baro_df.index =   baro_df['units'].str.strip(' ')+' '+baro_df['description']
        baro_df = baro_df.T
        baro_dict = dict(baro_df.ix['value'])
        ##
        all_meas_list = []
        for d in [meas_dict,batt_dict,baro_dict]:
            for j in d.iteritems():
                all_meas_list.append(j)
        ## append to results table
        results_df = results_df.append(pd.DataFrame(dict(all_meas_list), index=[loc_time.strftime("%m/%d/%Y %H:%M")]))
    #results_df['in Water Level'].plot(title='Water Level (in)')
    print 'Data download complete!'
    print
    print results_df[['in Water Level',u'\xb0F Water Temperature',u'mS/cm EC',u' Sensor Metadata',u'% Battery Percent','mV Battery Voltage','kPa Reference Pressure',u'\xb0F Logger Temperature']]
    ## update with new data
    WL = WL_existing.append(results_df)
    ## Plot
#    fig,ax=plt.subplots(1,1,figsize=(12,6))
#    ax.set_title(site_name,fontsize=14,fontweight='bold')
#    ax.plot_date(pd.to_datetime(results_df.index),results_df['in Water Level'],marker='None',ls='-',c='blue')
#    if len(WL_existing)>0:
#        ax.plot_date(pd.to_datetime(WL_existing.index),WL_existing['in Water Level'],marker='None',ls='-',c='grey')
#    ax.legend()
#    ax.xaxis.set_major_formatter(DateFormatter('%m/%d/%Y'))# %H:%M'))
    ## Save raw data to csv
    WL[['in Water Level',u'°F Water Temperature',u'mS/cm EC',u' Sensor Metadata',u'% Battery Percent','mV Battery Voltage','kPa Reference Pressure',u'\xb0F Logger Temperature']].to_csv(maindir+'/Water_Level_data/'+site_name+'_raw_data_ZentraAPI.csv',encoding='utf-8')
#%%  
    
    
    
