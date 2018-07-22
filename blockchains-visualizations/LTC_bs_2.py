# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:55:28 2018
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from collections import Counter

#import time
#from datetime import date,timedelta
#import requests

sns.set(color_codes='Dark')
#plt.style.use('fivethirtyeight')

#%% load data, method 2
url_LTC_pool = 'https://www.litecoinpool.org/pools'

# Returns list of all tables on page
LTC_pool_tables = pd.read_html(url_LTC_pool)

# Select the third table
LTC_table_3 = LTC_pool_tables[3]

# manipulations to turn table to useful form
LTC_tb         = LTC_table_3.dropna(axis = 0, thresh = 3)
LTC_tb         = LTC_tb.drop([0])
LTC_tb.columns = LTC_table_3.iloc[0]

LTC_tb       = LTC_tb.iloc[::-1]
LTC_tb.index = np.arange(0,len(LTC_tb))

LTC_tb['Size']    = [int(x[:-2]) for x in LTC_tb['Size']]
LTC_tb['Txn']     = [int(x)      for x in LTC_tb['Txn']]
LTC_tb['Height']  = [int(x)      for x in LTC_tb['Height']]

#%%
fig_LTC = plt.figure(figsize=(17,9))

# subplot grid setup
ax_col = 6
ax_row = 3

ax_LTC_1 = plt.subplot2grid((ax_row, ax_col), (0, 0), colspan = 2)
ax_LTC_2 = plt.subplot2grid((ax_row, ax_col), (1, 0), colspan = 2)
ax_LTC_3 = plt.subplot2grid((ax_row, ax_col), (2, 0), colspan = 2)

ax_LTC_4 = plt.subplot2grid((ax_row, ax_col), (0, 2))
ax_LTC_5 = plt.subplot2grid((ax_row, ax_col), (1, 2))
ax_LTC_6 = plt.subplot2grid((ax_row, ax_col), (2, 2), colspan = 2)

ax_LTC_7 = plt.subplot2grid((ax_row, ax_col), (0, 3))
ax_LTC_8 = plt.subplot2grid((ax_row, ax_col), (1, 3))
ax_LTC_9 = plt.subplot2grid((ax_row, ax_col), (0, 4), colspan = 2)

ax_LTC_10 = plt.subplot2grid((ax_row,ax_col), (1, 4), colspan = 2)

ax_LTC_11 = plt.subplot2grid((ax_row, ax_col), (2, 4))

ax_LTC_12 = plt.subplot2grid((ax_row, ax_col), (2, 5))

plt.setp(ax_LTC_1.get_xticklabels(), visible=False)
plt.setp(ax_LTC_2.get_xticklabels(), visible=False)

#plt.setp(ax_LTC_4.get_xticklabels(), visible=False)
#plt.setp(ax_LTC_4.get_yticklabels(), visible=False)

#plt.setp(ax_LTC_5.get_xticklabels(), visible=False)
#plt.setp(ax_LTC_5.get_yticklabels(), visible=False)

#plt.setp(ax_LTC_6.get_xticklabels(), visible=False)
#plt.setp(ax_LTC_6.get_yticklabels(), visible=False)

plt.setp(ax_LTC_7.get_xticklabels(), visible=False)
plt.setp(ax_LTC_7.get_yticklabels(), visible=False)

#plt.setp(ax_LTC_8.get_xticklabels(), visible=False)
#plt.setp(ax_LTC_8.get_yticklabels(), visible=False)

#plt.setp(ax_LTC_9.get_xticklabels(), visible=False)
#plt.setp(ax_LTC_9.get_yticklabels(), visible=False)

plt.setp(ax_LTC_12.get_xticklabels(), visible=False)
plt.setp(ax_LTC_12.get_yticklabels(), visible=False)

#%% subplot 1 rolling average of block size
LTC_tb['size_mean_21'] = LTC_tb['Size'].rolling(
        window=21,center=True,min_periods=1).mean()

ax_LTC_1.set_title('Mean block size of every adjac. 21 blks vs.'
                       +'block height',fontsize=11)

# Two curves on the same plot
ax_LTC_1.plot(LTC_tb['Height'],
              LTC_tb['size_mean_21'],
              linewidth=1.2, color='blue')

ax_LTC_1.set_xlim(min(LTC_tb['Height']),
                  max(LTC_tb['Height']))
 
ax_LTC_1.set_ylim(0, max(LTC_tb['size_mean_21'])*1.2)
ax_LTC_1.set_ylabel('block size in kB', fontsize=11)


#%%
# subplot 2
# transaction rolling average per 21 blocks
LTC_tb['txn_mean_21'] = LTC_tb['Txn'].rolling(
        window=21,center=True,min_periods=1).mean()

# rolling average of transaction counts
ax_LTC_2.set_title('Mean txn count every adjac. 21 blks vs.'+
                   'block height',fontsize=11)

# Two curves on the same plot
ax_LTC_2.plot(LTC_tb['Height'],
              LTC_tb['txn_mean_21'],
              linewidth=1.2, color='r')

ax_LTC_2.set_xlim(min(LTC_tb['Height']),
                  max(LTC_tb['Height']))

ax_LTC_2.set_ylim(0, max(LTC_tb['txn_mean_21'])*1.2)
ax_LTC_2.set_ylabel('txn count',fontsize=11)

#%%
# subplot 3
# transaction rolling average per 21 blocks
LTC_tb['blksize_txn_ratio'] = (LTC_tb['Size']
/LTC_tb['Txn'])

LTC_tb['ratio_mean_21'] = LTC_tb['blksize_txn_ratio'].rolling(
        window=21,center=True,min_periods=1).mean()

# rolling average of transaction counts
ax_LTC_3.set_title('Mean blksize / txn ratio, averaged every adjac.'+
         '21 blks',fontsize=11)

# Two curves on the same plot
ax_LTC_3.plot(LTC_tb['Height'],
              LTC_tb['ratio_mean_21'],
              linewidth=1.2, color='green')

ax_LTC_3.set_xlim(min(LTC_tb['Height']),
                  max(LTC_tb['Height']))

ax_LTC_3.set_ylim(0, max(LTC_tb['ratio_mean_21'])*1.2)
ax_LTC_3.set_ylabel('blksize / txn ratio',fontsize=11)
ax_LTC_3.set_xlabel('block height',fontsize=11)

#%%
# subplot 4
# transaction distribution
sns.distplot(LTC_tb['Size'], kde = False, ax = ax_LTC_4,
             color ='b', bins=40)

ax_LTC_4.set_title('size (kB) histogram',fontsize=11)
ax_LTC_4.set_xlabel('')

#%%
# subplot 5
# transaction distribution
sns.distplot(LTC_tb['Txn'], kde = False, ax = ax_LTC_5,
             color='r', bins=40)

ax_LTC_5.set_title('transaction count histogram',fontsize=11)
ax_LTC_5.set_xlabel('')

# counting empty blocks
Em_Cn = LTC_tb['Txn'].value_counts().loc[1]

#%% Subplot 6 and 8, time info
# List Comprehension to alter time format
FMT = '%Y-%m-%d %H:%M'

del_t1 = [datetime.strptime(y, FMT) for y in LTC_tb['Timestamp (UTC)']]
del_t2 = [(z-del_t1[0]).seconds/60  for z in del_t1]
del_t3 = [del_t2[n] - del_t2[n-1] for n in range(1,len(del_t2))]

# del_t3 only has 499 elements, add in another at the begning, using
# "+" to combine lists
LTC_tb['del_t4'] = [0] + del_t3
LTC_tb['del_t5'] = LTC_tb['del_t4'].rolling(window=21,center=True,
               min_periods=1).mean()

ax_LTC_6.set_title('delta_t btw adja blks(21 blk mean)'+
         '21 blks',fontsize=11)

# Two curves on the same plot
# del_t5 is the 21 blokc average of the time difference between two
# blocks

ax_LTC_6.plot(LTC_tb['Height'],
              LTC_tb['del_t5'],
              linewidth = 1.2, color = 'purple')

ax_LTC_6.plot(LTC_tb['Height'],
              [2.5 for y in range(0,len(LTC_tb))],
              linewidth = 1.2, linestyle = '--', color = 'blue')

ax_LTC_6.set_xlim(min(LTC_tb['Height']),
                  max(LTC_tb['Height']))

ax_LTC_6.set_ylim(0, max(LTC_tb['del_t5'])*1.2)
ax_LTC_6.set_ylabel('minutes',fontsize=11)
ax_LTC_6.set_xlabel('block height',fontsize=11)

# time diff between adjacent blocks distribution
sns.distplot(LTC_tb['del_t4'], kde = False, ax = ax_LTC_8,
             color='orange')

ax_LTC_8.set_title('delta_t btw adjac blks histogram',fontsize=11)
ax_LTC_8.set_xlabel('')
#ax_LTC_8.set_xlim(0,10)

#%%
# Subplot 7, some stats
yp = list(np.arange(7,-1,-1))
yp = [x/10 for x in yp]

alignment = {'horizontalalignment': 'left', 
             'verticalalignment': 'baseline'}

# positions for the stats:
StatsTexts = ['height: ',
              'txns/blk, mean: ', 
              'txns/blk, median: ', 
              'txns/blk, max: ',
              'txns, 500 blks', 
              'blk size, mean:',
              'blk size, median: ',
              'blk size, max: ']

alignment2 = {'horizontalalignment': 'right', 
              'verticalalignment': 'baseline'}

StatsTexts2 = [str(np.max(LTC_tb['Height'])),
               str(format(np.mean(LTC_tb['Txn']),'.2f')),
               str(np.median(LTC_tb['Txn'])),
               str(np.max(LTC_tb['Txn'])),
               str(np.sum(LTC_tb['Txn'])),
               str(format(np.mean(LTC_tb['Size']),'.2f')),
               str(np.median(LTC_tb['Size'])),
               str(np.max(LTC_tb['Size']))]

#for k, ST1 in enumerate(StatsTexts):
#    t =   ax_LTC_7.text(0.1, yp[k]+0.15, StatsTexts[k], 
#                        family='calibri', **alignment)

# advanced List Comprehension
t = [ax_LTC_7.text(0.1, yp[k]+0.15, StatsTexts[k],
                   family='calibri', **alignment, fontsize = 11) 
    for k,ST1 in enumerate(StatsTexts)]

# family='calibri', **alignment2, color = 'green')
        
T = [ax_LTC_7.text(
        0.9, 
        yp[k]+0.15, 
        StatsTexts2[k], 
        family='calibri', 
        **alignment2, 
        color = 'black',
        fontsize=11
        ) 
    if k != 5 
    else 
    ax_LTC_7.text(
            0.9, 
            yp[k]+0.15, 
            StatsTexts2[k],
            family='calibri', 
            **alignment2, 
            color = 'blue',
            fontsize=11
            )
    for k,ST1 in enumerate(StatsTexts2)]
        
ax_LTC_7.grid(False)

#%% Subplot 9, using Seaborn module
# use List Comprehension to group empty/non-empty blocks
ind_of_common = 8

name_big_miner = [Counter(LTC_tb['Finder']).most_common(ind_of_common)[x][0] 
      for x in range(ind_of_common)]

LTC_tb['EMTY_stats']  = ['empty' if x == 1 else 'not empty' 
      for x in LTC_tb['Txn'] ]

LTC_tb['Finder2'] = [x if x in name_big_miner else 'other' 
      for x in LTC_tb['Finder']]

sns.countplot(x = 'Finder2', hue = 'EMTY_stats', data = LTC_tb, 
              order = name_big_miner + ['other'],
              hue_order = ['not empty','empty'],
              ax = ax_LTC_9);

sns.set_palette("husl")
ax_LTC_9.legend(loc=1, borderaxespad=0.)
ax_LTC_9.set_xticklabels(name_big_miner+['other'],rotation=30, fontsize = 8.5)
ax_LTC_9.set_xlabel('')
ax_LTC_9.set_ylabel('block count')
    
#%% Subplot 11 empty bar chart
ind2 = [1,2]
ax_LTC_11.bar(ind2,
              [Em_Cn/len(LTC_tb)*100,(len(LTC_tb)-Em_Cn)/len(LTC_tb)*100], 
              width = 0.2,
              color = ['chocolate','forestgreen'])
             
ax_LTC_11.set_ylabel('percent')
ax_LTC_11.set_xlabel('')

ax_LTC_11.set_xlim(0, 3)
ax_LTC_11.set_xticklabels(['','empty','non-empty'],rotation=0, fontsize = 8.5)

ax_LTC_11.set_yticks(np.arange(0, 110, 10))
ax_LTC_11.set_ylim(0, 100)

#%% percentage of empty blocks

LTC_pivoted = LTC_tb.pivot_table(index = 'Finder2', columns = 'EMTY_stats', 
                                 values = 'Txn',aggfunc='count').reset_index()
LTC_pivoted = LTC_pivoted.fillna(0)
LTC_pivoted['summed'] = [
        LTC_pivoted['empty'].iloc[x] + 
        LTC_pivoted['not empty'].iloc[x] 
        for x in np.arange(0,len(LTC_pivoted))]

LTC_pivoted['EMTY_perc'] = [LTC_pivoted['empty'].iloc[x] / 
            LTC_pivoted['summed'].iloc[x]*100 
            for x in np.arange(0,len(LTC_pivoted))]

sns.barplot(x='Finder2', y='EMTY_perc', data=LTC_pivoted, ax = ax_LTC_10,
            order = name_big_miner + ['other'],
            color = 'chocolate')

ax_LTC_10.set_xticklabels(name_big_miner+['other'],rotation=30,fontsize = 8.5)
ax_LTC_10.set_xlabel('')
ax_LTC_10.set_ylabel('% blocks are empty')

#%%
mean_txn_tb = LTC_tb.pivot_table(index = 'Finder2', 
                                 aggfunc = {'mean','sum'})[
                                 'Size'].sort_values('sum',ascending=False)

alignment = {'horizontalalignment': 'left', 
             'verticalalignment': 'baseline'}

alignment2 = {'horizontalalignment': 'right', 
             'verticalalignment': 'baseline'}

for i in range(0,len(mean_txn_tb)):
    ax_LTC_12.text(0.5, (0.85 - 0.1*i), mean_txn_tb.index[i], 
                   family='calibri', **alignment, fontsize = 11)
    
    ax_LTC_12.text(3.5, (0.85 - 0.1*i),str(
            format(mean_txn_tb['mean'].iloc[i],
                   '.2f')), family='calibri', **alignment2, fontsize = 11, 
                   color = 'chocolate')

ax_LTC_12.set_ylabel('')
ax_LTC_12.set_xlim(0,4)
ax_LTC_12.set_title('Mean block size by pools')
ax_LTC_12.grid(False)

#%% set tight layout
fig_LTC.tight_layout()
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(100,90,1700,900)
fig_LTC.patch.set_facecolor('lightgrey')

#%%
sns.set(style="ticks")

# Initialize the figure with a logarithmic x axis
fig_LTC_2, ax_2 = plt.subplots(figsize=(7, 6))

# Plot the orbital period with horizontal boxes
sns.boxplot(x="Size", y="Finder2", data = LTC_tb, 
            whis = np.inf, palette = "coolwarm", ax = ax_2,
            order = name_big_miner + ['other'])

# Add in points to show each observation
sns.swarmplot(x = "Size", y = "Finder2", data = LTC_tb,
              size=2, color=".3", linewidth=0, ax = ax_2,
              order = name_big_miner + ['other'])

# Tweak the visual presentation
ax_2.set_ylabel('')
ax_2.xaxis.grid(True)
ax_2.set_title('box- and swarm- plots for block size distributions ')
sns.despine(trim=True, left=True)
fig_LTC_2.tight_layout()