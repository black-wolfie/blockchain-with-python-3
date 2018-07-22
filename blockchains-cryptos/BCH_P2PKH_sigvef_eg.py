# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 21:46:19 2018
By Wolfie
"""
import BCH_P2PKH_sigvef as bs0

address = 'bitcoincash:qpqsd7rc25ndsrgvymggz30xgvd07drlzc0jazdmhm'
signature = ('HPDs1TesA48a9up4QORIuub67VHBM37X66skAYz0Esg23gdfMu'+
             'CTYDFORc6XGpKZ2/flJ2h/DUF569FJxGoVZ50=')
message = 'test message'

bs0.sig_vef_P2PKH(address, signature, message)


#%%
# address doesn't have to start with "bitcoincash:" prefix
address2 = "qqnuzaypfgjy5edva0fs6a8634er0xz89yuuptm60y"
message2 = "test message"
signature2 = ("IPn9bbEdNUp6+bneZqE2YJbq9Hv5aNILq9E" + 
             "5eZoMSF3/fBX4zjeIN6fpXfGSGPrZyKfHQ/c/kTSP+NIwmyTzMfk=")
bs0.sig_vef_P2PKH(address2, signature2, message2)

#%%
address3 = "bitcoincash:qztlw8trrudklvnekmpv2pmwendtpap5qy4cpdr0x5"
message3 = ("Pretty cool stuff, this thing called Electron Cash."+
            " A nice wallet overall.")
sig3     = ("H2d6YNCrNiZ2LTFzFwfWWs1cFGPoSKJIvvGbNc/wlp6JE+7Mmve2"+
            "kosUc3lAwk3XlAmj9ee1bzAKlDRuJq0/BiU=")
bs0.sig_vef_P2PKH(address3, sig3, message3)