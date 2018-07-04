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

    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

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

def hash_160(public_key):
    md = hashlib.new('ripemd160')
    md.update(hashlib.sha256(public_key).digest())
    return md.digest()

def Hash(data):
    # first hash, encode the string message data
    hash_1st = hashlib.sha256(data.encode()).digest()
    # the result of the first hash is already a bytes-object
    hash_2nd = hashlib.sha256(hash_1st).digest()
    
    return hash_2nd

# character set for Base32 encoder
CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'

def b32encode(inputs):
    out = ''
    for char_code in inputs:
        out += CHARSET[char_code]
    return out

def prefix_expand(prefix):
    # as per description, convert "bitcoincash" prefix and, add one 0 at end
    # 0x1f = 31
    return [ord(x) & 0x1f for x in prefix] + [0]

def calculate_cksum(prefix, payload):
    poly = polymod(prefix_expand(prefix) + payload + [0, 0, 0, 0, 0, 0, 0, 0])
    out = list()
    for i in range(8):
        out.append((poly >> 5 * (7 - i)) & 0x1f)
    return out

def polymod(values):
    chk = 1
    generator = [
        (0x01, 0x98f2bc8e61),
        (0x02, 0x79b76d99e2),
        (0x04, 0xf33e5fb3c4),
        (0x08, 0xae2eabe2a8),
        (0x10, 0x1e4f43e470)]
    for value in values:
        top = chk >> 35
        chk = ((chk & 0x07ffffffff) << 5) ^ value
        for i in generator:
            if top & i[0] != 0:
                chk ^= i[1]
    return chk ^ 1

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret
