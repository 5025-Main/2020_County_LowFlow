# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 12:03:49 2020

@author: alex.messina
"""

maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'

HvF = pd.read_csv(maindir + 'Ancillary_files/' + 'HvF-90degweir.csv',index_col=1)
HvF.index = np.round(HvF.index,3)

datadir = maindir + 'Flow_Output_Excel_files/'

for d in [f for f in os.listdir(datadir) if f.endswith('.xlsx')]:
    print d
    site_name = d.split('-working draft.xlsx')[0]
    print site_name
    if site_name !='CAR-059':
        WL =  pd.read_excel(maindir + 'Flow_Output_Excel_files/' + d, sheetname= site_name+'-all flow',index_col=0)
        
        def hvf(x):
            try:
                level = HvF.loc[x,'Level (in)']
                try:
                    if len(HvF.loc[x,'Level (in)']) >= 1:
                        level = HvF.loc[x,'Level (in)'].values[0]
                except:  
                    pass
                    
                #print level
            except:
                level = np.nan
            return level
        
        WL['Level_in'] = WL['Flow compound weir (gpm)'].apply(lambda x: hvf(x))
        
        WL['Flow_gpm'] = WL['Flow compound weir (gpm)']
        
        WL[['Level_in','Flow_gpm']].to_csv(maindir+'Level_and_Flow_output/'+site_name+'_level_and_flow.csv')
