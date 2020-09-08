# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:34:33 2020

@author: alex.messina
"""
#%%

datadir = 'C:/Users/alex.messina/Desktop/'

df = pd.read_csv(datadir+ 'Datetime, Flow_gpm and Site ID.csv',index_col=0)
df['Time'] = [pd.to_datetime(x).time() for x in df.index]


plt.figure(figsize=(10,7))
t = sorted(df['Time'].unique())


# find the range
max1 = df.groupby(df['Time']).max()
min1 = df.groupby(df['Time']).min()

# plot the range
plt.fill_between(t, min1['Flow_gpm'].values.ravel(), max1['Flow_gpm'].values.ravel(), color='grey',label='Max/Min Flow (cfs), All Years')

# plot the mean 
plt.plot(t, df.groupby(df['Time'])['Flow_gpm'].mean(), color ='k',lw=2,label='Mean Flow (cfs)')
plt.plot(t, df.groupby(df['Time'])['Flow_gpm'].median(), color ='b',lw=2,label='Median Flow (cfs), All Years',ls='-')

plt.xlabel('Time of Day')
plt.ylabel('Flow (gpm)')
#plt.xlim((df['Time'].min(),df['Time'].max()))
plt.ylim(min1['Flow_gpm'].values.min(), max1['Flow_gpm'].values.max() * 1.25)

labels = t
[x.strftime("%H:%M") for x in t]
plt.xticks(t[::24], labels[::24], rotation='vertical')


plt.legend()
   
    
plt.suptitle('Max/Min Flows',fontsize=14)
plt.tight_layout()
plt.subplots_adjust(top=0.9)
