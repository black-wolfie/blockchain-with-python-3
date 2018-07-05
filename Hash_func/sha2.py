# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:53:28 2018
"""
BLOCKSIZE = 4000000
def sha2_lately(n):
    import hashlib
    import os
    from glob import glob

    h_sha256 = hashlib.sha256()
    files = glob("*.*")
    files.sort(key=os.path.getmtime)
    files = files[::-1]
    
    for x in range(0,n):
        h_sha256 = hashlib.sha256()

        try:
            afile = open(files[x], 'rb')
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                h_sha256.update(buf)
                buf = afile.read(BLOCKSIZE)
            print("SHA2-256 hash of", files[x], ":")
            print(h_sha256.hexdigest())
            print("")
        except PermissionError:
            return "some default data"

def sha2_name(names):
    import hashlib
    from glob import glob
    
    h_sha256 = hashlib.sha256()
    files = glob(names)
    n = len(files)
    files = files[::-1]
    
    for x in range(0,n):
        h_sha256 = hashlib.sha256()
        with open(files[x], 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                h_sha256.update(buf)
                buf = afile.read(BLOCKSIZE)

        print("SHA2-256 hash of", files[x], ":")
        print(h_sha256.hexdigest())
        print("")

def sha2():
    runfile(r'G:/My Drive/Python_codes_shared/Preloaded_funcs/sha2_GUI.py')
