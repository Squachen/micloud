# -----------------------------------------------------------
# Library to login to xiaomi cloud and get device info.
#
# (C) 2020 Sammy Svensson
# Released under MIT License
# email sammy@ssvensson.se
# -----------------------------------------------------------

import time
import random
import sys
import hashlib, hmac, base64
import string
from urllib.parse import urlparse

from micloud.micloudexception import MiCloudException


def get_random_agent_id():
        letters = 'ABCDEF'
        result_str = ''.join(random.choice(letters) for i in range(13))
        return result_str


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def gen_nonce():
    millis = int(round(time.time() * 1000))
    b = (random.getrandbits(64) - 2**63).to_bytes(8, 'big', signed=True)
    part2 = int(millis / 60000)
    b += part2.to_bytes(((part2.bit_length()+7)//8), 'big')
    return base64.b64encode(b).decode('utf-8')


def signed_nonce(ssecret, nonce):
    m = hashlib.sha256()
    m.update(base64.b64decode(bytes(ssecret, 'utf-8')))
    m.update(base64.b64decode(bytes(nonce, 'utf-8')))
    base64_bytes = base64.b64encode(m.digest())
    return base64_bytes.decode('utf-8')


def gen_signature(url, signed_nonce, nonce, params):
    if not signed_nonce or len(signed_nonce) == 0:
        raise MiCloudException("signed_nonce is required.")

    exps = []
    if url:
        uri = urlparse(url)
        exps.append(uri.path)

    exps.append(signed_nonce)
    exps.append(nonce)

    if params:
        for key in sorted (params) : 
            exps.append("%s=%s" % (key, params.get(key)))
    
    sign = ""
    first = True
    for s in exps:
        if not first:
            sign = sign + "&"
        else:
            first = False
        
        sign = sign + s

    signature = hmac.new(base64.b64decode(bytes(signed_nonce, 'utf-8')), msg = bytes(sign, 'utf-8'), digestmod = hashlib.sha256).digest()
    base64_bytes = base64.b64encode(signature)
    return base64_bytes.decode('utf-8')