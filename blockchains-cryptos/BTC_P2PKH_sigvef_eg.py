# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:46:11 2018
"""

import BTC_P2PKH_sigvef as bv

# verifying two P2PKH Bitcoin signed messages
address = 'bitcoin:16vqGo3KRKE9kTsTZxKoJKLzwZGTodK3ce'
signature = ('HPDs1TesA48a9up4QORIuub67VHBM37X66skAYz0Esg23gdfMu'+
        'CTYDFORc6XGpKZ2/flJ2h/DUF569FJxGoVZ50=')
message = 'test message'

bv.sig_vef_P2PKH(address, signature, message)

address2 = "14dD6ygPi5WXdwwBTt1FBZK3aD8uDem1FY"
message2 = "test message"
signature2 = ("IPn9bbEdNUp6+bneZqE2YJbq9Hv5aNILq9E" + 
             "5eZoMSF3/fBX4zjeIN6fpXfGSGPrZyKfHQ/c/kTSP+NIwmyTzMfk=")
bv.sig_vef_P2PKH(address2, signature2, message2)
