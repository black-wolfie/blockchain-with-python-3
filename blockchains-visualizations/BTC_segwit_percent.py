# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 12:52:26 2018
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def main():
    segwit_url = ("https://www.blockchair.com/bitcoin/blocks?fields=id,"+
                  "hash,time,transaction_count,witness_count&q=time(20"+
                  "17-09-01..)&export=csv")
    
    
    Table_segwit = pd.read_csv(segwit_url, delimiter=',')
    
    #%%
    Table_segwit['s_to_t_ratio'] = (Table_segwit['witness_count']/
                Table_segwit['transaction_count'])
    
    Table_segwit['ratio_144'] = Table_segwit['s_to_t_ratio'].rolling(
            144, min_periods = 1, center = True).mean()
    
    #%%
    
    sns.set(color_codes = "Dark")
    
    fig0, ax0 = plt.subplots(1,1,figsize = (8,6))
    ax0.plot(Table_segwit['id'],Table_segwit['ratio_144'])

if __name__ == "__main__":
    main()
