# -*- coding: utf-8 -*-
# Verifying BTC messages for Python 3!
# original Python 2 file: 
# https://github.com/stequald/bitcoin-sign-message/blob/master/signmessage.py
# usages:
"""
import BTC_P2PKH_sigvef as bv

address = '16vqGo3KRKE9kTsTZxKoJKLzwZGTodK3ce'
signature = ('HPDs1TesA48a9up4QORIuub67VHBM37X66skAYz0Esg23gdfMu'+
        'CTYDFORc6XGpKZ2/flJ2h/DUF569FJxGoVZ50=')
message = 'test message'

bv.sig_vef_P2PKH(address, signature, message)

address2 = "14dD6ygPi5WXdwwBTt1FBZK3aD8uDem1FY"
message2 = "test message"
signature2 = ("IPn9bbEdNUp6+bneZqE2YJbq9Hv5aNILq9E" + 
             "5eZoMSF3/fBX4zjeIN6fpXfGSGPrZyKfHQ/c/kTSP+NIwmyTzMfk=")
bv.sig_vef_P2PKH(address2, signature2, message2)

"""

# the code below is 'borrowed' almost verbatim from electrum,
# https://gitorious.org/electrum/electrum
# and is under the GPLv3.

import ecdsa
import base64
import hashlib
from ecdsa.util import string_to_number
from mod_sqrt import modular_sqrt
from b58encode import b58encode
from BTC_hash import Hash, hash_160

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
p_US  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r_US  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

b_US  = 0x0000000000000000000000000000000000000000000000000000000000000007
a_US  = 0x0000000000000000000000000000000000000000000000000000000000000000

Gx_US = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy_US = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

curve_secp256k1 = ecdsa.ellipticcurve.CurveFp( p_US, a_US, b_US )

generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, Gx_US, 
                                                Gy_US, r_US )

oid_secp256k1 = (1,3,132,0,10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, 
                               generator_secp256k1, oid_secp256k1 ) 

addrtype = 0

# from 
# http://eli.thegreenplace.net/2009/03/07/
# computing-modular-square-roots-in-python/

def msg_magic(message):
    return "\x18Bitcoin Signed Message:\n" + chr( len(message) ) + message

def public_key_to_bc_address(public_key):
    h160 = hash_160(public_key)
    vh160 = chr(addrtype).encode() + h160
    
    hash_1st = hashlib.sha256(vh160).digest()
    hash_2nd = hashlib.sha256(hash_1st).digest()
    
    addr = vh160 + hash_2nd[0:4]
    return b58encode(addr)

def encode_point(pubkey, compressed=False):
    order = generator_secp256k1.order()
    p = pubkey.pubkey.point
    x_str = ecdsa.util.number_to_string(p.x(), order)
    y_str = ecdsa.util.number_to_string(p.y(), order)
    
    if compressed:
        return chr(2 + (p.y() & 1)).encode() + x_str
    else:
        return chr(4).encode() + x_str + y_str

def sig_vef_P2PKH(address, signature, message):
    """ See http://www.secg.org/download/aid-780/sec1-v2.pdf for the math """
    from ecdsa import numbertheory, ellipticcurve, util
    curve = curve_secp256k1
    G = generator_secp256k1
    order = G.order()
    
    # extract r,s from signature
    sig = base64.b64decode(signature)
    if len(sig) != 65: raise BaseException("Wrong encoding")
    r,s = util.sigdecode_string(sig[1:], order)
    
    nV = sig[0]
    
    if nV < 27 or nV >= 35:
        print("False")
    if nV >= 31:
        compressed = True
        nV -= 4
    else:
        compressed = False
    
    recid = nV - 27
    # 1.1
    # must use int for x, or x turns into a float
    x = r + recid //2 * order
    
    # 1.3
    alpha = ( x * x * x  + curve.a() * x + curve.b() ) % curve.p()
    beta = modular_sqrt(alpha, curve.p())
    y = beta if (beta - recid) % 2 == 0 else curve.p() - beta
    
    # 1.4 the constructor checks that nR is at infinity
    R = ellipticcurve.Point(curve, x, y, order)
    
    # 1.5 compute e from message:
    h = Hash( msg_magic( message ) )
    e = string_to_number(h)
    minus_e = -e % order
    
    # 1.6 compute Q = r^-1 (sR - eG)
    inv_r = numbertheory.inverse_mod(r,order)
    Q = inv_r * ( s * R + minus_e * G )
    
    public_key = ecdsa.VerifyingKey.from_public_point( Q, curve = SECP256k1 )
    
    # check that Q is the public key
    public_key.verify_digest(sig[1:], h, 
                             sigdecode = ecdsa.util.sigdecode_string)
    
    # check that we get the original signing address
    addr = public_key_to_bc_address(encode_point(public_key, compressed))
    addr = "bitcoin:" + addr
    
    if address[0:8] != "bitcoin:":
        address = "bitcoin:" + address
    
    if address == addr:
        print('The signature is valid')
    else:
        print('The signature is NOT valid')
