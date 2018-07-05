# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:44:13 2018
"""

import hashlib

def Hash(data):
#    print("Hash input is ", data)
#    print(hashlib.sha256(data.encode()).digest())
    
    # first hash, encode the string message data
    hash_1st = hashlib.sha256(data.encode()).digest()
    # the result of the first hash is already a bytes-object
    hash_2nd = hashlib.sha256(hash_1st).digest()
    
    return hash_2nd

def hash_160(public_key):
    md = hashlib.new('ripemd160')
    md.update(hashlib.sha256(public_key).digest())
    return md.digest()