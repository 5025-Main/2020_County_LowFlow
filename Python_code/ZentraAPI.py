# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:51:41 2019

@author: alex.messina
"""
import pandas as pd
import numpy as np
import datetime as dt
from pytz import timezone
import json
import urllib2

def zentra_json_parser(json_obj, logger_port):
    ## Start with blank dataframe for results
    results_df = pd.DataFrame()
    ## define port number of CTD data
    port_reference_number = logger_port+1 ## need to add 1 I think
    
    ## Test first row to get the Port Number
    sensors = pd.DataFrame(json_obj['device']['timeseries'][0]['configuration']['sensors'])
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
        
        ## Extract measurement data using the defined port number (+1)
        try:
            water_level_data = filter(lambda x: x[0]['description']=='Water Level',row[3:])[0]
            meas_df = pd.DataFrame(water_level_data)
            ## Construct headers using units and parameter name
            meas_df.index =   meas_df['units'].str.strip(' ')+' '+meas_df['description']
            ## Transpose rows to column headers
            meas_df = meas_df.T
            meas_dict = dict(meas_df.ix['value'])
        
        except:
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
        
        all_meas_list = []
        for d in [meas_dict,batt_dict,baro_dict]:
            for j in d.iteritems():
                all_meas_list.append(j)

        ## append to results table
        results_df = results_df.append(pd.DataFrame(dict(all_meas_list), index=[loc_time]))
    
    return results_df

def getDeviceReadings(site_name,start_time_loc,device_df):
    print 'Downloading data from Zentra API for site: ' + site_name
    print ' starting at '+start_time_loc.strftime("%m/%d/%Y %H:%M")
    ## API log in credentials
    user = "alex.messina@woodplc.com"
    user_password = "Mactec101"
    ## Device data on Serial number, password, and Port that probe is plugged into
    #device_df = pd.DataFrame.from_csv(maindir + 'Ancillary_files/Meter_SN_pwd_list.csv')
    logger_port = device_df.ix[site_name]['Port']
    device_serial_number = device_df.ix[site_name]['Serial Number']
    device_password = device_df.ix[site_name]['Password']
    ## API token parameters
    ip = "zentracloud.com"
    key_name= 'AlexMessina'
    token =  '1a45a3456373971b5d1120ab9a9953e731f13402'
    ## Format start time
    start_time_utc = start_time_loc.astimezone(timezone('UTC'))
    start_time  = int((start_time_utc-dt.datetime(1970,1,1,0,0,tzinfo=timezone('UTC'))).total_seconds())
    
    ## Construct url for API call
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
    print 'Downloading and formatting data....please wait...'
    df = zentra_json_parser(readings_json, logger_port)
    
    df['in Water Level'].plot(title='Water Level (in)')
    print 'Data download complete!'
    
    # Examples of accessing data
    #print json.dumps(readings_json, sort_keys=True, indent=4)
    #print "get_readings_ver: ", json.dumps(readings_json['get_readings_ver'])
    #print "created: ", json.dumps(readings_json['created'])
    #print "device: ", json.dumps(readings_json['device'])
    #print "device_info: ", json.dumps(readings_json['device']['device_info'])

    
    
    return df[['in Water Level',u'°F Water Temperature',u'mS/cm EC',u' Sensor Metadata',u'% Battery Percent','mV Battery Voltage','kPa Reference Pressure',u'\xb0F Logger Temperature']]


#if __name__ == "__main__":
#    
#    ## TESTING
#    site_name = 'CAR-007'
#    start_time_loc = dt.datetime(2020,5,1,0,0)
#    
#    ## Format for UTC
#    mytz = timezone('US/Pacific')
#    start_time_loc = mytz.normalize(mytz.localize(start_time_loc,is_dst=True))
#    
#    ## Call Zentra API to get data from start time to current
#    df = getDeviceReadings(site_name, start_time_loc)
#    ## Save to csv
#    df.to_csv(maindir+'Water_Level_data/'+site_name+'.csv',encoding='utf-8')


#%%
