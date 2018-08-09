# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 16:03:23 2018
"""

from binascii import hexlify, unhexlify
b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58decode(s):
    """Decode a base58-encoding string, returning bytes"""
    if not s:
        return b''

    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        if c not in b58_digits:
            raise 'invalid base 58 format with invalid character'
            
        digit = b58_digits.index(c)
        n += digit

    # Convert the integer to bytes
    h = '%x' % n
    if len(h) % 2:
        h = '0' + h
    res = unhexlify(h.encode('utf8'))

    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == b58_digits[0]: pad += 1
        else: break
    return b'\x00' * pad + res
