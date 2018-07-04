# -*- coding: utf-8 -*-
# for Python 3!
# original Python 2 file: https://github.com/stequald/bitcoin-sign-message/blob/master/signmessage.py
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

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
p_US  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r_US  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

b_US  = 0x0000000000000000000000000000000000000000000000000000000000000007
a_US  = 0x0000000000000000000000000000000000000000000000000000000000000000

Gx_US = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy_US = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

curve_secp256k1 = ecdsa.ellipticcurve.CurveFp( p_US, a_US, b_US )

generator_secp256k1 = ecdsa.ellipticcurve.Point( curve_secp256k1, Gx_US, 
                                                Gy_US, r_US )

oid_secp256k1 = (1,3,132,0,10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, 
                               generator_secp256k1, oid_secp256k1 ) 

addrtype = 0

# from 
# http://eli.thegreenplace.net/2009/03/07/
# computing-modular-square-roots-in-python/

def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
    must be an odd prime.
    
    Solve the congruence of the form:
    x^2 = a (mod p)
    And returns x. Note that p - x is also a root.
    
    0 is returned is no square root exists for
    these a and p.
    
    The Tonelli-Shanks algorithm is used (except
    for some simple cases in which the solution
    is known from an identity). This algorithm
    runs in polynomial time (unless the
    generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    
    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1
        
    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
        
    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #
    
    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    
    print("s is", s)
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
            
        if m == 0:
            return x
        
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m
        
def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
    Euler's criterion. p is a prime, a is
    relatively prime to p (if p divides
    a, then a|p = 0)
    
    Returns 1 if a has a square root modulo
    p, -1 otherwise.
    """
#    print("a is ", a)
#    print("divide by 2 is", (p - 1) / 2)
#    print("p is ", p)
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
    """ encode v, which is a string of bytes, to base58.		
    """

    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        long_value += (256**i) * c

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break

    return (__b58chars[0]*nPad) + result

def msg_magic(message):
    return "\x18Bitcoin Signed Message:\n" + chr( len(message) ) + message

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

#def hash_160_to_bc_address(h160):
#    vh160 = chr(addrtype) + h160
#    h = Hash(vh160)
#    addr = vh160 + h[0:4]
#    return b58encode(addr)

def public_key_to_bc_address(public_key):
    h160 = hash_160(public_key)
#    print(h160)
    vh160 = chr(addrtype).encode() + h160
    
    hash_1st = hashlib.sha256(vh160).digest()
    hash_2nd = hashlib.sha256(hash_1st).digest()
    
    addr = vh160 + hash_2nd[0:4]
#    print(vh160)
#    print(hash_2nd)
    
    return b58encode(addr)

def encode_point(pubkey, compressed=False):
    order = generator_secp256k1.order()
    p = pubkey.pubkey.point
    x_str = ecdsa.util.number_to_string(p.x(), order)
    y_str = ecdsa.util.number_to_string(p.y(), order)
#    print("x_str is", x_str)
#    print("y_str_is", y_str)
    
    if compressed:
        return chr(2 + (p.y() & 1)).encode() + x_str
    else:
        return chr(4).encode() + x_str + y_str
    
#    if compressed:
#        return chr(2 + (p.y() & 1)) + x_str
#    else:
#        return chr(4) + x_str + y_str

#def sign_message(private_key, message, compressed=False):
#    
#    public_key = private_key.get_verifying_key()
#    signature = private_key.sign_digest( Hash( msg_magic( message ) ), 
#                                        sigencode = ecdsa.util.sigencode_string )
#    address = public_key_to_bc_address(encode_point(public_key, compressed))
#    
#    assert public_key.verify_digest( signature, Hash( msg_magic( message ) ), 
#                                    sigdecode = ecdsa.util.sigdecode_string)
#    for i in range(4):
#        nV = 27 + i
#        if compressed:
#            nV += 4
#        sig = base64.b64encode( chr(nV) + signature )
#        try:
#            if verify_message( address, sig, message):
#                return sig
#        except:
#            continue
#    else:
#        raise BaseException("error: cannot sign message")



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
    
    #    print(sig)
    #    print(len(sig))
    #    print(sig[0])
    #    nV = ord(sig[0])
    
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
    
    #    print('alpha is ', alpha)
    #    print('beta is ', beta)
    #    print('')
    #    print('y is ', y)
    
    # 1.4 the constructor checks that nR is at infinity
    R = ellipticcurve.Point(curve, x, y, order)
    
    # 1.5 compute e from message:
#    a_1 = msg_magic( message )
#    print(msg_magic( message ))
    
    h = Hash( msg_magic( message ) )
    e = string_to_number(h)
    minus_e = -e % order
    
    # 1.6 compute Q = r^-1 (sR - eG)
    inv_r = numbertheory.inverse_mod(r,order)
    Q = inv_r * ( s * R + minus_e * G )
    
    # Q = inv_r * (tuple([s*i for i in R]) + tuple([minus_e*j for j in G]))
    #print('')
    #print("Q is ", Q)
    
    public_key = ecdsa.VerifyingKey.from_public_point( Q, curve = SECP256k1 )
    
    # check that Q is the public key
    public_key.verify_digest( sig[1:], h, sigdecode = ecdsa.util.sigdecode_string)
    
    # check that we get the original signing address
    addr = public_key_to_bc_address(encode_point(public_key, compressed))
    
    print("")
    
    if address == ('1' + addr):
        print('The signature is valid')
    else:
        print('The signature is not valid')
