# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:29:50 2018
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date,timedelta
from collections import Counter

def main():
    sns.set(color_codes='Dark')
    
    n = 4
    days_b4     = date.today() - timedelta(n)
    days_b4_str = days_b4.strftime('%Y-%m-%d')
    
    
    url_ETH_string = ("https://api.blockchair.com/ethereum/blocks?q=time(" + 
                      days_b4_str + 
                      "..)&fields=id,time,uncle_count,"+
                      "transaction_count,size,"+
                      "gas_used,gas_limit&export=csv")
    
    tb_ETH = pd.read_csv(url_ETH_string, delimiter=',')
    tb_ETH['size'] = tb_ETH['size']/1000
    
    #%%
    tb_ETH['time'] = pd.to_datetime(tb_ETH['time'])
    
    tb_ETH = tb_ETH.rename(columns={'size': 'size_kB',
                                    'id':   'Height',
                                    'transaction_count': 'Txn',
                                    'uncle_count':'uncles'})
    
    # .csv goes most recent to least recent, need to reverse this
    tb_ETH = tb_ETH.iloc[::-1]
    tb_ETH.index = np.arange(0,len(tb_ETH))
    
    # Rolling average of each entry of size_kB, becomes size_mean21
    tb_ETH['size_mean150'] = tb_ETH['size_kB'].rolling(
            window=150,center=True,min_periods=1).mean()
    
    tb_ETH['Txn_mean150'] = tb_ETH['Txn'].rolling(
            window=150,center=True,min_periods=1).mean()
    
    tb_ETH['uncles_sum150'] = tb_ETH['uncles'].rolling(
            window=150,center=True,min_periods=1).sum()
    
    #%%
    fig_ETH = plt.figure(figsize=(17,9))
    
    # subplot grid setup
    ax_col = 6
    ax_row = 3
    
    ax_ETH_1 = plt.subplot2grid((ax_row, ax_col), (0, 0), colspan = 2)
    ax_ETH_2 = plt.subplot2grid((ax_row, ax_col), (1, 0), colspan = 2)
    ax_ETH_3 = plt.subplot2grid((ax_row, ax_col), (2, 0), colspan = 2)
    
    ax_ETH_4 = plt.subplot2grid((ax_row, ax_col), (0, 2))
    ax_ETH_5 = plt.subplot2grid((ax_row, ax_col), (1, 2))
    ax_ETH_6 = plt.subplot2grid((ax_row, ax_col), (2, 2), colspan = 2)
    
    ax_ETH_7 = plt.subplot2grid((ax_row, ax_col), (0, 3))
    ax_ETH_8 = plt.subplot2grid((ax_row, ax_col), (1, 3))
    ax_ETH_9 = plt.subplot2grid((ax_row, ax_col), (0, 4), colspan = 2)
    
    ax_ETH_10 = plt.subplot2grid((ax_row,ax_col), (1, 4), colspan = 2)
    
    ax_ETH_11 = plt.subplot2grid((ax_row, ax_col), (2, 4))
    
    ax_ETH_12 = plt.subplot2grid((ax_row, ax_col), (2, 5))
    
    plt.setp(ax_ETH_1.get_xticklabels(), visible=False)
    plt.setp(ax_ETH_2.get_xticklabels(), visible=False)
    
    plt.setp(ax_ETH_7.get_xticklabels(), visible=False)
    plt.setp(ax_ETH_7.get_yticklabels(), visible=False)
    
    plt.setp(ax_ETH_12.get_xticklabels(), visible=False)
    plt.setp(ax_ETH_12.get_yticklabels(), visible=False)
    
    #%% subplot 1: rolling average of block size
    ax_ETH_1.set_title('Mean block size of every adjac. 150 blks vs.'
                           +'block height',fontsize=11)
    
    # Two curves on the same plot
    ax_ETH_1.plot(tb_ETH['Height'],
                  tb_ETH['size_mean150'],
                  linewidth=1.2, color='blue')
    
    ax_ETH_1.set_xlim(min(tb_ETH['Height']),
                      max(tb_ETH['Height']))
     
    ax_ETH_1.set_ylim(0, max(tb_ETH['size_mean150'])*1.2)
    ax_ETH_1.set_ylabel('block size in kB', fontsize=11)
    
    #%% subplot 2: rolling average of transaction counts
    ax_ETH_2.set_title('Mean txn count every adjac. 150 blks vs.'+
                       'block height', fontsize=11)
    
    # Two curves on the same plot
    ax_ETH_2.plot(tb_ETH['Height'],
                  tb_ETH['Txn_mean150'],
                  linewidth=1.2, color='r')
    
    ax_ETH_2.set_xlim(min(tb_ETH['Height']),
                      max(tb_ETH['Height']))
    
    ax_ETH_2.set_ylim(0, max(tb_ETH['Txn_mean150'])*1.2)
    ax_ETH_2.set_ylabel('txn count',fontsize=11)
    
    #%% rolling sum of uncle counts
    ax_ETH_3.set_title("uncle sum every 150 blocks",fontsize=11)
    
    # Two curves on the same plot
    ax_ETH_3.plot(tb_ETH['Height'],
                  tb_ETH['uncles_sum150'],
                  linewidth=1.2, color='green')
    
    ax_ETH_3.set_xlim(min(tb_ETH['Height']),
                      max(tb_ETH['Height']))
    
    ax_ETH_3.set_ylim(0, max(tb_ETH['uncles_sum150'])*1.2)
    ax_ETH_3.set_ylabel("uncle count every 150 blocks",fontsize=11)
    ax_ETH_3.set_xlabel('block height',fontsize=11)
    
    for tick in ax_ETH_3.get_xticklabels():
            tick.set_rotation(30)

if __name__ == "__main__":
    main()
