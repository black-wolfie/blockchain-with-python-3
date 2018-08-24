# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 21:46:19 2018
By Wolfie
"""
import BCH_P2PKH_sigvef as bs0

address = 'bitcoincash:qpqsd7rc25ndsrgvymggz30xgvd07drlzc0jazdmhm'
signature = ('HPDs1TesA48a9up4QORIuub67VHBM37X66skAYz0Esg23gdfMuCTYDFORc6XGpKZ2/flJ2h/DUF569FJxGoVZ50=')
message = 'test message'

bs0.sig_vef_P2PKH(address, signature, message)


#%%
# address doesn't have to start with "bitcoincash:" prefix
address2 = "qqnuzaypfgjy5edva0fs6a8634er0xz89yuuptm60y"
message2 = "test message"
signature2 = ("IPn9bbEdNUp6+bneZqE2YJbq9Hv5aNILq9E5eZoMSF3/fBX4zjeIN6fpXfGSGPrZyKfHQ/c/kTSP+NIwmyTzMfk=")
bs0.sig_vef_P2PKH(address2, signature2, message2)

#%%
address3 = "bitcoincash:qztlw8trrudklvnekmpv2pmwendtpap5qy4cpdr0x5"
message3 = ("Pretty cool stuff, this thing called Electron Cash."+
            " A nice wallet overall.")
sig3     = ("H2d6YNCrNiZ2LTFzFwfWWs1cFGPoSKJIvvGbNc/wlp6JE+7Mmve2kosUc3lAwk3XlAmj9ee1bzAKlDRuJq0/BiU=")
bs0.sig_vef_P2PKH(address3, sig3, message3)

#%% BUCash signing verification, 1.4.0.0
import json
address4 = "bitcoincash:qrdvmdluf2s5cf08wcp9h2ja8lqt5peq35y56z4s7s"
message4 = { 'files': { 'BUcash-1.4.0.0-arm32.tar.gz': 'b84b798c8b4554252d5f291158be585644870ffc7ad2bdbdf5a248c4bf972735',
             'BUcash-1.4.0.0-arm64.tar.gz': '4d8b82bf4a547a0cd0ef9e02942f6ca9de99005419b4d7674a89814ea9362a35',
             'BUcash-1.4.0.0-linux32.tar.gz': 'd4edd79eb40a32621c084ff5c5bb99e7ace29ab68f19db5482182ea993486e70',
             'BUcash-1.4.0.0-linux64.tar.gz': '1d9ea2e84e197f190a8a62bff615d8a7ead3972783b037920628397106121fa1',
             'BUcash-1.4.0.0-osx.dmg': '3e009418cf1bf80397e49957a77ff4a7ce1edf2d9df8cc5088e93130fa9c9a18',
             'BUcash-1.4.0.0-osx.tar.gz': 'be09d1dd0e66a50ffd2a1a3292a1fe304ee823e80d997312d4e1aab53b5d7330',
             'BUcash-1.4.0.0-osx64.tar.gz': 'e8d457ecd8731f6c8c888a18a6c39eebd07b01e37ff5696c55b2b0983eed8599',
             'BUcash-1.4.0.0-win32-setup.exe': 'cc276f182810f377a602af94fab2ea5681ae9617f83e2caed2fa273517cbfbfc',
             'BUcash-1.4.0.0-win32.zip': '40c22c0784421bab740573caac9887696fa494c5c0d674a38b2886ca317a19c2',
             'BUcash-1.4.0.0-win64-setup.exe': '31a14c92041cf5c084456b5aebdd614677e3db54e7f3e30d04e5d85b55d16927',
             'BUcash-1.4.0.0-win64.zip': 'afe9be56aa0deac7b3b2adace8006ad2fd04003f0fc41e97eb0e81e7169a3029'},'program': 'BitcoinUnlimitedCash','version': '1.4.0.0'}
message4 = json.dumps(message4)
sig4     = ("H+GpGnu6Efkw8uB/EdH8MdUKkMXgMIVcBDJfdRbmlxYsX/tvNhG6QEOFG5fWWgzrFS96PAwuzuOHB9ngHg7sNBA=")
bs0.sig_vef_P2PKH(address4, sig4, message4)
