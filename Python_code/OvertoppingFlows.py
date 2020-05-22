# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 14:36:38 2018

@author: alex.messina
"""
#%%
from matplotlib import pyplot as plt
import numpy as np


def get_weir_dims(site_name,weir_dims):
    vnotch_in= weir_dims.ix[site_name][['h2']].values
    width_in = weir_dims.ix[site_name][['b2']].values + weir_dims.ix[site_name][['c1']].values + weir_dims.ix[site_name][['c2']].values
    vnotch_ft, width_ft = vnotch_in/12., width_in/12.
    print() 
    print('Site: '+site_name)
    print('V-notch height: '+str(vnotch_in)+' in. Width: '+str(width_in) +' in.')
    print('V-notch height: '+"%.2f"%vnotch_ft+' ft. Width: '+"%.2f"%width_ft +' ft.')
    return vnotch_ft, width_ft

#%%


def CTRSC_compound_weir(site_name,WL,weir_dims,plot_timeseries=False,plot_scatter=False):
    ## Get weir dims from sheet
    vnotch_in= float(weir_dims.ix[site_name][['h2']].values[0])
    b2 = float(weir_dims.ix[site_name][['b2']].values[0])
    b1 = float(weir_dims.ix[site_name][['b1 (left)']].values[0]) + float(weir_dims.ix[site_name][['b1 right (if different)']].values[0])
    c1 = float(weir_dims.ix[site_name][['c1']].values[0])
    c2 = float(weir_dims.ix[site_name][['c2']].values[0])
    h1 = float(weir_dims.ix[site_name][['h1']].values[0])
    
    print vnotch_in, b2, b1, c1,c2, h1
        
    #vnotch_cm, width_cm, c1_cm, c2_cm, h1_cm = vnotch_in * 2.54, (b1+b2) * 2.54, c1*2.54, c2*2.54, h1*2.54 
    vnotch_m, width_m, c1_m, c2_m, h1_m = vnotch_in * 0.0254, (b1+b2) * 0.0254, c1*0.0254, c2*0.0254, h1*0.0254
    ## Calculate weir geometry for equation
    b2_cm = b2 * 2.54
    b1_cm = b1 * 2.54
    b1_m, b2_m = b1_cm/100, b2_cm/100
    ## Constants
    Ctd, Crd = 0.579,	0.590
    
    ## Get Level data
    df = WL[['Level_in','Flow_gpm_v']]
    df.columns = ['Level_in','Flow_gpm_v']
    df['Level_in'] = df['Level_in'].where(df['Level_in'] >= 0., np.nan)
    
    ## Format equation inputs
    df['h2(m)'] = df['Level_in'] * 0.0254 ## Height above V
    df['h2_eff(m)'] =  df['h2(m)'] + 0.0008 ## Effective head
    df['h1(m)'] = df['h2(m)'] - vnotch_m ## Height above Horizontal crest
    df['h1_eff(m)'] = df['h1(m)']  + 0.0008 ## Effective head
    
    
    ## Calculate discharge for compound weir - Discussion of “Design and Calibration of a Compound Sharp-Crested Weir” by J. Martínez, J. Reca, M. T. Morillas, and J. G. López,”, 2005
    df['Flow_m3s_ctrsc'] =     ((8./15.) * Ctd * ((2.*9.81)**0.5) * (np.tan(np.radians(90.)/2.)) * (df['h2_eff(m)']**2.5 - df['h1_eff(m)']**2.5))    +     ((2./3.) * Crd * ((2.*9.81)**0.5) * (2 * b1_m) * (df['h1(m)']**1.5))
    ## change from m3/s to gpm
    df['Flow_gpm_ctrsc'] = df['Flow_m3s_ctrsc'] * 15850.372483753
    
    ## Add the flow from the compound weir equation where it is higher than the standard v-notch equation
    df['Flow_gpm'] = df['Flow_gpm_ctrsc'].where((df['Flow_gpm_ctrsc'] > df['Flow_gpm_v']), df['Flow_gpm_v'])

    ## PLOTTING
    if plot_timeseries == True:
        fig, (level,flow) = plt.subplots(2,1,sharex=True,figsize=(12,6))
        ## PLOT LEVEL
        ## Plot total Water Level Height
        level.plot_date(df.index,df['h2(m)'] * 100. /2.54,ls='-',marker='.',label='Level inches',c='b')
        ## Plot overtopping Water Level 
        level.plot_date(df.index,(df['h1(m)'] + vnotch_m)* 100. /2.54,ls='-',marker='.',label='Height above horizontal crest (in)',c='r')
        ## Add line at vnotch height
        level.axhline(vnotch_in,c='r')
        level.set_ylabel('Level_in)',fontweight='bold')
        
        ## PLOT FLOW
        flow.plot_date(df.index,df['Flow_gpm'],ls='-',marker='.',label='Flow: HvF and ctrsc',c='r')
        flow.plot_date(df.index,df['Flow_gpm_v'],ls='-',marker='.',label='Flow just V',c='b')
#        flow.plot_date(df.index,df['Flow (gpm) compound'],ls='-',marker='.',label='Flow compound',c='g')
        flow.set_ylabel('Flow (gpm)',fontweight='bold')
        
        ## fmt
        level.legend(), flow.legend()
        plt.tight_layout()
        
        
    if plot_scatter == True:
        fig, ax = plt.subplots(1,1,figsize=(10,10))
        ax.plot(df['Level_in'], df['Flow_gpm_ctrsc'],ls='None',marker='.',c='r',label='Compound weir equation')
        ax.plot(df['Level_in'], df['Flow_gpm_v'],ls='None',marker='.',c='b',label='V-notch equation')
        ax.set_xlabel('Level (inches)',fontweight='bold'), ax.set_ylabel('Flow (gpm)',fontweight='bold')
        ax.legend(loc='upper left')
        plt.tight_layout()

    return df['Flow_gpm'].astype('float').round(3)

    
    
#CTRSC_compound_weir('CAR-059',WL,weir_dims,plot_timeseries=True,plot_scatter=True)    
    
    
    
    
    
    
    
    
    
    
    
    
