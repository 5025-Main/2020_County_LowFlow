# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 12:30:18 2016

@author: alex.messina
"""
import pandas as pd
import requests
from BeautifulSoup import BeautifulSoup

def get_OneRain_data(rain_gauge_name,start_date, end_date,Rain_gauge_info,time_bin='86400'): 
    ## Date range from start_date and now
    daterange = pd.date_range(start_date.replace('-',''),end_date.replace('-',''),freq='D')
    ## Rain gauge parameters for building url
    RG_ID = str(Rain_gauge_info.ix[rain_gauge_name]['rain_gauge_id'])
    print 'ID: '+ RG_ID
    RG_SERIAL = Rain_gauge_info.ix[rain_gauge_name]['rain_gauge_serial']
    print 'SERIAL :'+RG_SERIAL
    RG_DEV_ID = str(Rain_gauge_info.ix[rain_gauge_name]['rain_gauge_device_id'])
    print 'DEVICE ID: '+ RG_DEV_ID
    RG_DEV_SERIAL = Rain_gauge_info.ix[rain_gauge_name]['rain_gauge_device_serial']
    print 'DEVICE SERIAL: '+ RG_DEV_SERIAL
    print '\n'

    try:
        ## Verify rain gauge name
        url = 'https://sandiego.onerain.com/sensor.php?time_zone=US%2FPacific&site_id='+RG_ID+'&site='+RG_SERIAL+'&device_id='+RG_DEV_ID+'&device='+RG_DEV_SERIAL+'&bin='+time_bin+'&range=Custom+Range&legend=true&thresholds=true&refresh=off&show_raw=true&show_quality=true&data_start='+start_date+'+00%3A00%3A00&data_end='+end_date+'+23%3A59%3A59'
        
        s = requests.get(url).content
        
        soup = BeautifulSoup(s)
        
        try:
            print 'Grabbing data for Rain gauge: '+rain_gauge_name
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
                                #print 'Failed'
                                #print h4_tag
                                #print '\n'
                                pass
                        ## Get rain data
                        for h4_tag in soup.findAll('h4',{'class':'list-group-item-heading'}):
                            try:
                                rain_val =  h4_tag.text.split('&nbsp;')[0]
                                #print rain_val
                                rain_vals.append(float(rain_val))
                            except:
                                #print 'Failed'
                                #print h4_tag
                                #print '\n'
                                pass
                        rain_data_df = pd.DataFrame({'Rain_in':rain_vals},index=pd.to_datetime(times)).sort_index()
                        rain_data_df = rain_data_df.resample('D').sum()
                        
                        #rain_data_df.to_csv(maindir+'Rain_data/'+Rain_gauge_name+'_daily.csv')
            except Exception as e:
                print (e)
                pass
        except Exception as e:
                print (e)
                pass
    except Exception as e:
                print (e)
                pass
    return rain_data_df
            

        
