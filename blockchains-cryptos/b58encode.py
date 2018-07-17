# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:42:18 2018
"""

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
# some preps for b58encoder
iseq = lambda s: s
bseq = bytes
buffer = lambda s: s.buffer

def b58encode_int(i, default_one=True):
    '''Encode an integer using Base58'''
    if not i and default_one:
        return alphabet[0]
    string = ""
    while i:
        i, idx = divmod(i, 58)
        string = alphabet[idx] + string
    return string


def b58encode(v):
    '''Encode a string using Base58'''
    if not isinstance(v, bytes):
        raise TypeError("a bytes-like object is required, not '%s'" %
                        type(v).__name__)

    origlen = len(v)
    v = v.lstrip(b'\0')
    newlen = len(v)

    p, acc = 1, 0
    for c in iseq(reversed(v)):
        acc += p * c
        p = p << 8

    result = b58encode_int(acc, default_one=False)

    return (alphabet[0] * (origlen - newlen) + result)