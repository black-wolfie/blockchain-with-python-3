# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 12:52:26 2018
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def main():
    segwit_url = ("https://api.blockchair.com/bitcoin/blocks?"+
                  "fields=id,transaction_count,witness_count&q"+
                  "=time(2019-01-01..)&export=csv")
    
    print(segwit_url)
    Table_segwit = pd.read_csv(segwit_url, header = None, skiprows = 1,
                               sep = ',', names = ['id', 'transaction_count',
                                                   'witness_count'])
    
    #%%
    Table_segwit['s_to_t_ratio'] = (Table_segwit['witness_count']/
                                    Table_segwit['transaction_count'])
    
    Table_segwit['ratio_144'] = Table_segwit['s_to_t_ratio'].rolling(
            144, min_periods = 1, center = True).mean()
    
    sns.set(color_codes = "Dark")
    
    fig0, ax0 = plt.subplots(1,1,figsize = (8,6))
    ax0.plot(Table_segwit['id'],Table_segwit['ratio_144'])

if __name__ == "__main__":
    main()
