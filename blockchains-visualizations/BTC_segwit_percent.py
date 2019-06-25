# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 12:52:26 2018
"""
import matplotlib.pyplot as plt
import seaborn as sns; import pandas as pd
from datetime import date, timedelta, datetime

def main():
    sns.set(color_codes=True)
    t0 = date.today()
    t_today = t0
    n = 6
    
    for i in range(n):
        t1 = t0.replace(day=1)
        t2 = t1 - timedelta(days=1)
        t0 = t2 
    t0 = t0.replace(day=1)
    
    All_months = ['Jan','Feb','Mar','Apr','May','Jun',
                  'Jul','Aug','Sep','Oct','Nov','Dec']
    All_months2 = All_months + All_months + All_months
    All_months3 = All_months2[(
            12 + t_today.month - (n+1)
            ) : (
            24 + t_today.month - (n+1)
            )]

    url_string_3 = ('https://api.blockchair.com/bitcoin/blocks?'+
                    'q=time('+str(t0)+'+00:00:00..)&'+
                    'fields=id,time,transaction_count,witness_count&export=csv')
    
    Table_SW = pd.read_csv(url_string_3, header = None, skiprows = 1,
                           sep = ',', names = ['id', 'time',
                                               'transaction_count',
                                               'witness_count'])
    
    #%% grouping and plotting
    FMT = '%Y-%m-%d %H:%M:%S'
    
    Table_SW['t1'] = [datetime.strptime(y, FMT) for y in Table_SW['time']]
    
    #% .dt.date works for Pandas datetime Series
    Table_SW_2 = Table_SW.groupby([Table_SW['t1'].dt.date]).mean()
    
    Table_SW_2['Month'] = [x.month for x in Table_SW_2.index]
    Table_SW_2['Day']   = [x.day   for x in Table_SW_2.index]
    Table_SW_2['ratio'] = (Table_SW_2['witness_count'] / 
                           Table_SW_2['transaction_count'])
    Table_SW_2['ratio'] = Table_SW_2['ratio'].round(3)*1e2
    
    fig_SW_date, ax1 = plt.subplots(1, 1, figsize=[17,4])
    
    # pivoting for block size in kB
    Table_SW_3 = Table_SW_2.pivot(index='Month', 
                                  columns='Day', 
                                  values='ratio')
    
    for i in range(n):
        if Table_SW_3.index[i] != Table_SW_3.index[i+1] - 1:
            Table_SW_3 = pd.concat((Table_SW_3.iloc[ (i+1):, :],
                                    Table_SW_3.iloc[:(i+1),  :]), axis = 0)
            break
    
    Table_SW_3.index = [list(zip(Table_SW_3.index, All_months3))[x][1] 
                            for x in range(0,len(Table_SW_3))]
    
    sns.heatmap(Table_SW_3, annot=True, fmt='g', linewidths=0.2, 
                ax = ax1, cmap="YlGnBu")
    
    ax1.set_title('Segwit daily transaction percentage of all transactions')
    fig_SW_date.tight_layout()    
    
#%%
if __name__ == "__main__":
    main()