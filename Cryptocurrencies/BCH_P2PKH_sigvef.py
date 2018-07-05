import ecdsa
import base64
from ecdsa.util import string_to_number
from mod_sqrt import modular_sqrt
from BTC_hash import Hash, hash_160
from BCH_cash_addr_tools import b32encode, calculate_cksum, convertbits


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

def msg_magic(message):
    return "\x18Bitcoin Signed Message:\n" + chr( len(message) ) + message

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
    public_key.verify_digest( sig[1:], h, sigdecode = ecdsa.util.sigdecode_string)
    
    # check that we get the original signing address
    addr = public_key_to_Cash_Addr(encode_point(public_key, compressed))
    
    print("")
    
    if address == addr:
        print('The signature is valid')
    else:
        print('The signature is not valid')
        
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

def public_key_to_Cash_Addr(public_key):
    # public key is hashed with SHA256 and RipeMD160
    h160 = hash_160(public_key)
  
    # here is where Cash Addr differs from Bitcoin mainnet
    # double SHA256 hash is not used for checksum
    # you obtain the payload, then apply base32 encoder to it
    
    # payload = prefix + h160 hash + checksum
    version_bit = chr(addrtype).encode()
    prefix = "bitcoincash"
    payload = version_bit + h160
    
    # converting bits
    payload = convertbits(payload, 8, 5)
    checksum = calculate_cksum(prefix, payload)
    
    # https://github.com/oskyk/cashaddress/blob/master/cashaddress/convert.py
    return prefix + ':' + b32encode(payload + checksum)

