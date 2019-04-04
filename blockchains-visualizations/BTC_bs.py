# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 10:19:01 2018
"""
#%% Importing modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date,timedelta,datetime

def main():
    #import seaborn as sns
    #import scipy as sp
    #from pandas.io.json import json_normalize
    # number of the most recent days you want to query
    sns.set(color_codes=True)
    n = 4
    days_b4     = date.today() - timedelta(n)
    days_b4_str = days_b4.strftime('%Y-%m-%d')
    
    #%%
    url_string = ('https://api.blockchair.com/bitcoin/blocks?q=time('
    +days_b4_str+'..)&fields='
    +'id,hash,time,guessed_miner,transaction_count,output_total,'
    +'output_total_usd,fee_total,fee_total_usd,fee_per_kb_usd,'
    +'witness_count,input_count,fee_total,size,weight&export=csv') 
    
    # Converting .csv into Pandas Dataframe with read_csv
#    Table_BTC_1 = pd.read_csv(url_string, delimiter='t\,', header = 0)
    Table_BTC_1 = pd.read_csv(url_string, header = None, skiprows = 1,
                                sep = ',', 
                                names = ['id', 'hash', 'time', 'guessed_miner', 
                                         'transaction_count','output_total', 
                                         'output_total_usd', 'fee_total', 
                                         'fee_total_usd', 'fee_per_kb_usd', 
                                         'witness_count', 'input_count', 
                                         'fee_total.1', 'size', 'weight'])
    
    Table_BTC_1 = Table_BTC_1.rename(columns={'size': 'size_B',
                                    'id':   'Height',
                                    'transaction_count': 'Txn'})
    
    # .csv goes most recent to least recent, need to reverse this
    Table_BTC_1 = Table_BTC_1.iloc[::-1]
    Table_BTC_1.index = Table_BTC_1.index.values[::-1]
    
    # Rolling average of each entry of size_B, becomes size_mean21
    Table_BTC_1['size_mean21'] = Table_BTC_1['size_B'].rolling(
            window=21,center=True,min_periods=1).mean()
    
    #%% Plotting everything in 6 subplots (2-by-3).
    
    fig, axarr = plt.subplots(2, 4, figsize=[16,8])
    
    # Layout settings
    fig.subplots_adjust(top=0.962, bottom=0.081, left=0.073, right=0.959,
                        hspace=0.285, wspace=0.383)
    
    # subplot 1
    axarr[(0,0)].set_title('Mean block size of every adjac. 21 blks vs.'
                           +'block height',fontsize=10)
    
    # Two curves on the same plot
    axarr[(0,0)].plot(Table_BTC_1.Height,Table_BTC_1.size_mean21/1e3,
                  linewidth=1.2, color='blue')
    axarr[(0,0)].plot([min(Table_BTC_1.Height)-1e3, max(Table_BTC_1.Height)+1e3],
                  [1000, 1000],'r:',linewidth=0.7)
    
    axarr[(0,0)].set_xlim(min(Table_BTC_1.Height),max(Table_BTC_1.Height))
    axarr[(0,0)].set_ylim(0, max(Table_BTC_1.size_mean21/1e3)*1.2)
    axarr[(0,0)].set_ylabel('block size in kB')
    axarr[(0,0)].set_xlabel('block height')
    
    #%% Subplot 2
    # block height vs. total fee per block, BTC
    axarr[(0,1)].set_title('Total Bitcoin fee per block',fontsize=10)
    axarr[(0,1)].set_ylabel('Fees in BTC')
    axarr[(0,1)].set_xlabel('block height')
    axarr[(0,1)].plot(Table_BTC_1['Height'],
                    Table_BTC_1['fee_total']/1e8,'b.',markersize=5)
    
    #%% Subplot 3, using Seaborn
    sns.distplot(Table_BTC_1['fee_total']/1e8, kde = True, ax = axarr[(0,2)],
                 bins=40)
    
    #axarr[0,2].set_title('Distribution of miner fee per block',fontsize=10)
    axarr[(0,2)].set_ylabel('block count')
    axarr[(0,2)].set_xlabel('miner fee per block')
    
    #%% Subplot 4, using Seaborn
    sns.distplot(Table_BTC_1['Txn'], kde = False, ax = axarr[(1,0)],
                 color='m', bins=40)
    
    #axarr[1,0].set_title('Txns per block',fontsize=10)
    axarr[(1,0)].set_ylabel('block count')
    axarr[(1,0)].set_xlabel('transaction counts')
    
    #%% Subplot 5, using Seaborn, query non-empty blks first
    NonEmptyBlks = Table_BTC_1['size_B'].loc[Table_BTC_1['Txn'] != 1]
    sns.distplot(NonEmptyBlks/1e3, kde = False, ax = axarr[(1,1)],
                 color='g', bins=40)
    
    #axarr[1,0].set_title('Txns per block',fontsize=10)
    axarr[(1,1)].set_ylabel('block count')
    axarr[(1,1)].set_xlabel('distribution of block size, kB')
    
    #%% Subplot 6, some stats
    yp = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
    
    alignment = {'horizontalalignment': 'left', 
                 'verticalalignment': 'baseline'}
    
    # positions for the stats:
    StatsTexts = ['height: ',
                  'txns/blk, mean: ', 
                  'txns/blk, median: ', 
                  'txns/blk, max: ',
                  'txns, last '+str(n)+' days:', 
                  'blk size, mean:',
                  'blk size, median: ',
                  'blk size, max: ']
    
    alignment2 = {'horizontalalignment': 'right', 
                  'verticalalignment': 'baseline'}
    
    StatsTexts2 = [str(np.max(Table_BTC_1.Height)),
                   str(format(np.mean(Table_BTC_1.Txn),'.2f')),
                   str(np.median(Table_BTC_1.Txn)),
                   str(np.max(Table_BTC_1.Txn)),
                   str(np.sum(Table_BTC_1.Txn)),
                   str(format(np.mean(Table_BTC_1.size_B)/1e3,'.2f')),
                   str(np.median(Table_BTC_1.size_B)/1e3),
                   str(np.max(Table_BTC_1.size_B)/1e3)]
    
    for k, StatsTexts in enumerate(StatsTexts):
        t = axarr[(1,2)].text(0+0.1,   yp[k]-0.1, StatsTexts, 
                            family='calibri', **alignment)
    
    for k, StatsTexts in enumerate(StatsTexts2): 
        t = axarr[(1,2)].text(0.8+0.1, yp[k]-0.1, StatsTexts2[k], 
                            family='calibri', **alignment2)
    axarr[(1,2)].grid(False)
    plt.setp(axarr[(1,2)].get_xticklabels(), visible=False)
    plt.setp(axarr[(1,2)].get_yticklabels(), visible=False)
    #%%
    FMT = '%Y-%m-%d %H:%M:%S'
    
    del_t1 = [datetime.strptime(y, FMT) for y in Table_BTC_1['time']]
    del_t2 = [(z-del_t1[0]).seconds for z in del_t1]
    del_t3 = [del_t2[n] - del_t2[n-1] for n in range(1,len(del_t2))]
    del_t3 = [x for x in del_t3 if abs(x) <= 7200]
    
    sns.distplot(del_t3,kde = False, ax = axarr[(0,3)], color='g', bins=30)
    
    #axarr[0,3].set_xlim(0,3600)
    axarr[(0,3)].set_ylabel('block count')
    axarr[(0,3)].set_xlabel('distribution of time between blocks')
    
    #%% bar plot distribution of mining blocks
    mine_index = Table_BTC_1['guessed_miner'].value_counts().index
    sns.countplot(x = 'guessed_miner', data = Table_BTC_1, 
                  order = mine_index, ax = axarr[(1,3)]);
    axarr[(1,3)].set_ylabel("block count")
    axarr[(1,3)].set_xlabel("")
    
    #%% Set xtick/ytick sizes, for all subplots
    plt.setp([a.get_xticklabels() for a in fig.axes[:]], fontsize=8,
              rotation=60)
    plt.setp([a.get_yticklabels() for a in fig.axes[:]], fontsize=10)
    fig.patch.set_facecolor('lightgrey')
    
    #%% miner stats breakdown, weight
    sns.set(style="ticks")
    
    # Initialize the figure with a logarithmic x axis
    fig_BTC_2, ax_BTC_2 = plt.subplots(nrows = 1, ncols = 2, figsize=(14, 6))
    Table_BTC_1['weight_MB'] = Table_BTC_1['weight']/1e6
    
    # Plot the orbital period with horizontal boxes
    sns.boxplot(x="weight_MB", y="guessed_miner", data = Table_BTC_1, 
                palette = "coolwarm", ax = ax_BTC_2[(0)],
                order = mine_index)
    
    # Add in points to show each observation
    sns.swarmplot(x = "weight_MB", y = "guessed_miner", data = Table_BTC_1,
                  size=2, color=".3", linewidth=0, ax = ax_BTC_2[(0)],
                  order = mine_index)
    
    # Tweak the visual presentation
    ax_BTC_2[(0)].set_ylabel("")
    ax_BTC_2[(0)].set_xlabel("weight (MB)")
    ax_BTC_2[(0)].xaxis.grid(True)
    sns.despine(trim=True, left=True)
    
    # miner stats breakdown, block size
    Table_BTC_1['size_MB'] = Table_BTC_1['size_B']/1e6
    
    # Plot the orbital period with horizontal boxes
    sns.boxplot(x="size_MB", y="guessed_miner", data = Table_BTC_1, 
                palette = "coolwarm", ax = ax_BTC_2[(1)],
                order = mine_index)
    
    # Add in points to show each observation
    sns.swarmplot(x = "size_MB", y = "guessed_miner", data = Table_BTC_1,
                  size=2, color=".3", linewidth=0, ax = ax_BTC_2[(1)],
                  order = mine_index)
    
    ax_BTC_2[(1)].set_ylabel("")
    ax_BTC_2[(1)].set_xlabel("block size (MB)")
    ax_BTC_2[(1)].xaxis.grid(True)
    plt.xticks(np.arange(0, np.around(Table_BTC_1['size_MB'].max()), step=0.2))
    
    sns.despine(trim=True, left=True)
    fig_BTC_2.tight_layout()

if __name__ == "__main__":
    main()


