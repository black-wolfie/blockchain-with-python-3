# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 09:26:24 2018
"""
# Importing modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date,timedelta

def main():
    sns.set(color_codes=True)
    
    #import seaborn as sns
    #import scipy as sp
    #from pandas.io.json import json_normalize
    # number of the most recent days you want to query
    n = 4
    
    days_b4     = date.today() - timedelta(n)
    days_b4_str = days_b4.strftime('%Y-%m-%d')
    
    #%%
    url_bch_string = ('https://api.blockchair.com/bitcoin-cash/blocks?q=time('
    +days_b4_str+'..)&fields='
    +'id,hash,time,guessed_miner,transaction_count,output_total,'
    +'output_total_usd,fee_total,fee_total_usd,fee_per_kb_usd,'
    +'input_count,fee_total,size&export=csv')
    
    #%%
    # Converting .csv into Pandas Dataframe with read_csv
    Table_BCH_2 = pd.read_csv(url_bch_string, header = None, skiprows = 1,
                            sep = ',', 
                            names = ['id', 'hash', 'time', 'guessed_miner', 
                                     'transaction_count','output_total', 
                                     'output_total_usd', 'fee_total', 
                                     'fee_total_usd', 'fee_per_kb_usd', 
                                     'witness_count', 'input_count', 
                                     'fee_total.1', 'size', 'weight'])
    # Table_BCH_2 = pd.read_csv(url_bch_string, delimiter=',')
    
    Table_BCH_2 = Table_BCH_2.rename(columns={'size': 'size_B',
                                    'id':   'Height',
                                    'transaction_count': 'Txn'})
    
    # .csv goes most recent to least recent, need to reverse this
    Table_BCH_2 = Table_BCH_2.iloc[::-1]
    Table_BCH_2.index = Table_BCH_2.index.values[::-1]
    
    # Rolling average of each entry of size_B, becomes size_mean21
    Table_BCH_2['size_mean21'] = Table_BCH_2['size_B'].rolling(
            window=21,center=True,min_periods=1).mean()
    
    #%% Plotting everything in 6 subplots (2-by-3).
    
    fig, axarr = plt.subplots(2, 3, figsize=[13,8])
    
    # subplot 1
    axarr[0,0].set_title('Mean block size of every adjac. 21 blks vs.'
                           +'block height',fontsize=10)
    
    # Layout settings
    fig.subplots_adjust(top=0.962, bottom=0.081, left=0.073, right=0.959,
                        hspace=0.285, wspace=0.383)
    
    # subplot 1
    axarr[0,0].set_title('Mean block size of every adjac. 21 blks vs.'
                           +'block height',fontsize=10)
    
    # Two curves on the same plot
    axarr[0,0].plot(Table_BCH_2.Height, Table_BCH_2.size_mean21 / 1e3,
                    linewidth=1.2, color='blue')
    axarr[0,0].plot([min(Table_BCH_2.Height) - 1e3, max(Table_BCH_2.Height) + 1e3],
                    [1000, 1000],'r:', linewidth=0.7)
    
    axarr[0,0].set_xlim(min(Table_BCH_2.Height), max(Table_BCH_2.Height))
    axarr[0,0].set_ylim(0, max(Table_BCH_2.size_mean21 / 1e3) * 1.2)
    axarr[0,0].set_ylabel('block size in kB')
    axarr[0,0].set_xlabel('block height')
    
    #%% Subplot 2
    # block height vs. total fee per block, BCH
    axarr[0,1].set_title('Total Bitcoin fee per block',fontsize=10)
    axarr[0,1].set_ylabel('Fees in BCH')
    axarr[0,1].set_xlabel('block height')
    axarr[0,1].plot(Table_BCH_2['Height'],
                    Table_BCH_2['fee_total'] / 1e8, 'b.', markersize=5)
    
    #%% Subplot 3, using Seaborn
    sns.distplot(Table_BCH_2['fee_total'] / 1e8, kde = True, ax = axarr[0, 2],
                 bins=40)
    
    #axarr[0,2].set_title('Distribution of miner fee per block',fontsize=10)
    axarr[0,2].set_ylabel('block count')
    axarr[0,2].set_xlabel('miner fee per block')
    
    #%% Subplot 4, using Seaborn
    sns.distplot(Table_BCH_2['Txn'], kde = False, ax = axarr[1, 0],
                 color='m', bins=40)
    
    #axarr[1,0].set_title('Txns per block',fontsize=10)
    axarr[1,0].set_ylabel('block count')
    axarr[1,0].set_xlabel('transaction counts')
    
    #%% Subplot 5, using Seaborn, query non-empty blks first
    NonEmptyBlks = Table_BCH_2['size_B'].loc[Table_BCH_2['Txn'] != 1]
    sns.distplot(NonEmptyBlks/1e3, kde = False, ax = axarr[1,1],
                 color='g', bins=40)
    
    #axarr[1,0].set_title('Txns per block',fontsize=10)
    axarr[1,1].set_ylabel('block count')
    axarr[1,1].set_xlabel('distribution of block size, kB')
    
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
    
    StatsTexts2 = [str(np.max(Table_BCH_2.Height)),
                   str(format(np.mean(Table_BCH_2.Txn), '.2f')),
                   str(np.median(Table_BCH_2.Txn)),
                   str(np.max(Table_BCH_2.Txn)),
                   str(np.sum(Table_BCH_2.Txn)),
                   str(format(np.mean(Table_BCH_2.size_B) / 1e3, '.2f')),
                   str(np.median(Table_BCH_2.size_B) / 1e3),
                   str(np.max(Table_BCH_2.size_B) / 1e3)]
    
    for k, StatsTexts in enumerate(StatsTexts):
        t = axarr[1,2].text(0+0.1,   yp[k]-0.1, StatsTexts, 
                            family='calibri', **alignment)
    
    for k, StatsTexts in enumerate(StatsTexts2): 
        t = axarr[1,2].text(0.8+0.1, yp[k]-0.1, StatsTexts2[k], 
                            family='calibri', **alignment2)
    
    plt.setp(axarr[1,2].get_xticklabels(), visible=False)
    plt.setp(axarr[1,2].get_yticklabels(), visible=False)
    axarr[1,2].grid(False)
    
    #%% Set xtick/ytick sizes, for all subplots
    plt.setp([a.get_xticklabels() for a in fig.axes[:]], fontsize=8,
              rotation=60)
    plt.setp([a.get_yticklabels() for a in fig.axes[:]], fontsize=10)
    fig.patch.set_facecolor('lightgrey')
    
    #%% miner stats breakdown
    sns.set(style="ticks")
    
    # Initialize the figure with a logarithmic x axis
    fig_BCH_2, ax_BCH_2 = plt.subplots(figsize=(7, 6))
    Table_BCH_2['size_MB'] = Table_BCH_2['size_B']/1e6
    
    # Plot the orbital period with horizontal boxes
    sns.boxplot(x='size_MB', y='guessed_miner', data = Table_BCH_2, 
                palette = "coolwarm", ax = ax_BCH_2,
                order = Table_BCH_2['guessed_miner'].value_counts().index)
    
    # Add in points to show each observation
    sns.swarmplot(x = 'size_MB', y = 'guessed_miner', data = Table_BCH_2,
                  size=2, color=".3", linewidth=0, ax = ax_BCH_2,
                  order = Table_BCH_2['guessed_miner'].value_counts().index)
    
    # Tweak the visual presentation
    ax_BCH_2.set_ylabel("")
    ax_BCH_2.set_xlabel("size (MB)")
    ax_BCH_2.xaxis.grid(True)
    ax_BCH_2.set_title("box- and swarm- plots for block size distributions")
    sns.despine(trim=True, left=True)
    fig_BCH_2.tight_layout()

if __name__ == "__main__":
    main()