# Importing modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import date, timedelta, datetime

def main():
    sns.set(color_codes=True)
    t0 = date.today()
    t_today = t0
    
    for i in range(4):
        t1 = t0.replace(day=1)
        t2 = t1 - timedelta(days=1)
        t0 = t2 
    t0 = t0.replace(day=1)
    
    All_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    All_months2 = All_months + All_months + All_months
    All_months3 = All_months2[(12 + t_today.month - 5) : (24 + t_today.month - 5)]
    
    url_string_3 = ('https://api.blockchair.com/bitcoin-cash/blocks?'+
                    'q=time('+str(t0)+'+00:00:00..)'+
                    '&u=33c716b7-cf65-4b3b-8784-7f229f30e8cc&'+
                    'fields=id,time,transaction_count,input_count,size&export=csv')
    
    Table_BCH_2 = pd.read_csv(url_string_3, delimiter = ',')
    
    # grouping
    Table_BCH_2['size_kB'] = [x/1000 for x in Table_BCH_2['size']]
    
    FMT = '%Y-%m-%d %H:%M:%S'
    
    Table_BCH_2['t1'] = [datetime.strptime(y, FMT) for y in Table_BCH_2['time']]
    
    #% .dt.date works for Pandas datetime Series
    Table_BCH_3 = Table_BCH_2.groupby([Table_BCH_2['t1'].dt.date]).mean()
    
    Table_BCH_3['Month'] = [x.month for x in Table_BCH_3.index]
    Table_BCH_3['Day']   = [x.day   for x in Table_BCH_3.index]
    
    # plotting
    fig_BCH_date, axarr = plt.subplots(3, 1, figsize=[17,8])
    
    # pivoting for block size in kB
    Table_BCH_4 = Table_BCH_3.pivot(index='Month', columns='Day', values='size_kB')
    
    
    Table_BCH_4.index = [list(zip(Table_BCH_4.index, All_months3))[x][1] 
                         for x in range(0,len(Table_BCH_4))]
    
    Table_BCH_4 = Table_BCH_4.round(0)
    
    # fmt = 'g' is general formating
    sns.heatmap(Table_BCH_4, annot=True, fmt='g', linewidths=0.2, 
                ax = axarr[0], cmap="YlGnBu")
    
    axarr[0].set_title('Block size average, in kB')
    
    # pivoting for mean transaction counts
    Table_BCH_5 = Table_BCH_3.pivot(index='Month', columns='Day', 
                                    values='transaction_count')
    

    
    Table_BCH_5.index = [list(zip(Table_BCH_5.index,All_months3))[x][1] 
                         for x in range(0,len(Table_BCH_5))]
    Table_BCH_5 = Table_BCH_5.round(0)
    
    sns.heatmap(Table_BCH_5, annot=True, fmt='g', linewidths=0.2, 
                ax = axarr[1], cmap="YlGnBu")
    axarr[1].set_title('Mean Transaction Count')
    
    
    
    # pivoting for input_count
    Table_BCH_6 = Table_BCH_3.pivot(index='Month', columns='Day', 
                                    values='input_count')
    
    
    Table_BCH_6.index = [list(zip(Table_BCH_6.index,All_months3))[x][1] 
                         for x in range(0,len(Table_BCH_5))]
    
    Table_BCH_6 = Table_BCH_6.round(0)
    
    sns.heatmap(Table_BCH_6, annot=True, fmt='g', linewidths=0.2, 
                ax = axarr[2], cmap="YlGnBu")
    
    axarr[2].set_title('Mean Input Count')
    
    fig_BCH_date.tight_layout()

if __name__ == "__main__":
    main()