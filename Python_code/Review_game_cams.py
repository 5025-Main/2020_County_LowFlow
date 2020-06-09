# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 10:06:06 2020

@author: alex.messina
"""
import os
import pandas as pd
import datetime as dt
## Image tools
import matplotlib.image as mpimg
from scipy import ndimage
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import piexif


site_name = 'CAR-007'


maindir = 'C:/Users/alex.messina/Documents/GitHub/2020_County_LowFlow/'


## Local file
WL = pd.read_excel(maindir + 'Flow_Output_Excel_files/'+site_name+'-working draft.xlsx',sheetname=site_name+'-all flow',index_col=0) ## Excel file
WL['Flow_gpm'] = WL['Flow compound weir (gpm)']

## GitHub
WL = pd.read_csv('https://raw.githubusercontent.com/5025-Main/2020_County_LowFlow/master/Level_and_Flow_output/'+site_name+'_level_and_flow.csv')

#%%

def get_pic_date(pic_path):
    date_taken = piexif.load(pic_path)['Exif'][36867]
    return date_taken

print 'Site for camera...'+site_name
## Downloading photos from Google Photos
pic_dir = 'C:/Users/alex.messina/Downloads/'
pic_folder = '2020 '+site_name + '/'

#pic_dir = 'C:/Users/alex.messina/Desktop/Temporary_work_shit/County Weirs/Cameras/'
#pic_folder = 'CAR-007/'

## Compile DF of datetimes and picture file names
print ' compiling datetimes and picture file names....'
pic_datetimes = pd.DataFrame()
for pic in [os.listdir(pic_dir+pic_folder)][0]:
    print pic
    date_taken = get_pic_date(pic_dir+pic_folder+pic)

    print date_taken
    t = dt.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
    pic_datetimes = pic_datetimes.append(pd.DataFrame({'Pic filename':pic,'Date Taken':t},index=[t]))
print 'datetimes and picture file names....DONE'   


# define your images to be plotted
#pics = [os.listdir(pic_dir+pic_folder)][0][5000:] ## You can limit photos here

## Select by date
pics = pic_datetimes[pic_datetimes.index >= dt.datetime(2019,7,27,0,0)]['Pic filename']

# now the real code :) 
curr_pos = 0

def key_event(e):
    
    global curr_pos

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(pics)
    print 'key event '+str(curr_pos)
  
    ## Select pic
    picture_file = pic_dir + pic_folder+ pics[curr_pos]
    print 'Pic file: '+pics[curr_pos]
    ## Extract datetime of pic and format datetime
    date_taken = get_pic_date(picture_file)
    print 'Date taken: '+date_taken
    t = dt.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
    t_round5 = dt.datetime(t.year, t.month, t.day, t.hour,5*(t.minute // 5),0)
    ## Get flow and level data at time of pic
    flow_at_image = WL.ix[t_round5,'Flow_gpm']
    level_at_image = WL.ix[t_round5,'Level_in']
    
    ## Image
    ax1.cla()
    ax1.set_title('SITE: '+site_name+' Datetime: '+t.strftime('%m/%d/%y %H:%M') +' Pic: '+pics[curr_pos])
    img=mpimg.imread(picture_file)
    # from now on you can use img as an image, but make sure you know what you are doing!
    if site_name == 'CAR-070' or site_name=='SDR-064':
        rot_img=ndimage.rotate(img,degrees)
        imgplot=ax1.imshow(rot_img)
        
    else:
        imgplot=ax1.imshow(img)
    plt.show()
    
    ## Plot flow data
    ax2.cla()
    ax2.plot_date(WL.index,WL['Flow_gpm'],marker='None',ls='-',c='b',label='Flow compound weir')
    ax2.plot_date(t_round5, flow_at_image,marker='o',ls='None',c='b',label='Flow at picture='+"%.3f"%flow_at_image)
    
    ## Plot Level data   
    ax2_2.cla()
    if level_at_image <0 or np.isnan(level_at_image):
        level_color = 'r'
    elif level_at_image == 0:
        level_color='k'
    elif level_at_image>0:
        level_color='g'
    ax2_2.plot_date(WL.index, WL['Level_in'],marker='None',ls='-',c=level_color,label='Level (inches)')  
    ax2_2.plot_date(t_round5, level_at_image,marker='o',ls='None',c=level_color,label='Level at picture='+"%.2f"%level_at_image)
    ax2_2.set_ylim(-1, 6)
    ## Set plot limits
    ax2.set_xlim(t_round5 - dt.timedelta(hours=8), t_round5 + dt.timedelta(hours=8))
    ## Get flow data over a 24 hour surrounding period
    flow_over_interval = WL.ix[t_round5 - dt.timedelta(hours=8):t_round5 + dt.timedelta(hours=8),'Flow_gpm']
    ## y limits
    if flow_over_interval.min() == 0. and flow_over_interval.max() > 0.:
        ax2.set_ylim(-1.,flow_over_interval.max()*1.1)
    elif flow_over_interval.min() == 0. and flow_over_interval.max() == 0.:
            ax2.set_ylim(-3.,3.)
    else:
        ax2.set_ylim(flow_over_interval.min()*0.9,flow_over_interval.max()*1.1)
        
    ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%A \n %m/%d/%y %H:%M'))

    ax2.set_ylabel('Flow (gpm)'), ax2_2.set_ylabel('Level (inches)')

    ## Legends, they're all around
    ax2.legend(loc='upper left')
    ax2_2.legend(loc='upper right')
        
    fig1.canvas.draw()
    return



fig1, (ax1,ax2) = plt.subplots(2,1,figsize=(16,11))

fig1.canvas.mpl_connect('key_press_event', key_event)


picture_file = pic_dir + pic_folder+ pics[curr_pos]
date_taken = get_pic_date(pic_dir+pic_folder+pic)
t = dt.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
t_round5 = dt.datetime(t.year, t.month, t.day, t.hour,5*(t.minute // 5),0)
flow_at_image = WL.ix[t_round5,'Flow_gpm']
level_at_image = WL.ix[t_round5,'Level_in']

## Image
#ax1 = fig1.axes[0]
ax1.set_title('SITE: '+site_name+' Datetime: '+t.strftime('%m/%d/%y %H:%M'))
img=mpimg.imread(picture_file)
# from now on you can use img as an image, but make sure you know what you are doing!
if site_name in ['SDR-127']:
    degrees = -90
    rot_img=ndimage.rotate(img,degrees)
    imgplot=ax1.imshow(rot_img)
elif site_name in []:
    degrees = 90
    rot_img=ndimage.rotate(img,degrees)
    imgplot=ax1.imshow(rot_img)    
    
else: 
    imgplot=ax1.imshow(img)
plt.show()

ax2 = fig1.axes[1]
ax2.plot_date(WL.index,WL['Flow_gpm'],marker='None',ls='-',c='b',label='Flow compound weir')
ax2.plot_date(t_round5, flow_at_image,marker='o',ls='None',c='b',label='Flow at picture='+"%.3f"%flow_at_image)


## Level
ax2_2 = ax2.twinx()
if level_at_image <0  or np.isnan(level_at_image):
        level_color = 'r'
elif level_at_image == 0:
    level_color='k'
elif level_at_image>0:
    level_color='g'
ax2_2.plot_date(WL.index, WL['Level_in'],marker='None',ls='-',c=level_color,label='Level (inches)')
ax2_2.plot_date(t_round5, level_at_image,marker='o',ls='None',c=level_color,label='Level at picture='+"%.2f"%level_at_image)
ax2_2.set_ylim(-1, 6)

## Legends, they're all around
ax2.legend(loc='upper left')
ax2_2.legend(loc='upper right')

## Y labels
ax2.set_ylabel('Flow (gpm)'), ax2_2.set_ylabel('Level (inches)')


## x and y limits
ax2.set_xlim(t_round5 - dt.timedelta(hours=8), t_round5 + dt.timedelta(hours=8))
flow_over_interval = WL.ix[t_round5 - dt.timedelta(hours=8):t_round5 + dt.timedelta(hours=8),'Flow_gpm']
if flow_over_interval.min() == 0. and flow_over_interval.max() > 0.:
    ax2.set_ylim(-5.,flow_over_interval.max()*1.1)
elif flow_over_interval.min() == 0. and flow_over_interval.max() == 0.:
        ax2.set_ylim(-3.,3.)
else:
    ax2.set_ylim(flow_over_interval.min()*0.9,flow_over_interval.max()*1.1)
## X axis date format
ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%A \n %m/%d/%y %H:%M'))


plt.tight_layout()
