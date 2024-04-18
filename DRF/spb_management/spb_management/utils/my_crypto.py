import random

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import hashlib
import base64

class RSAFunc:
    def __init__(self, path='../static/pwd/private.pem'):
        private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEoAIBAAKCAQEAwSbE5jE8D7KwDizStHWygGbTIWMMF41jGYoYBqVg5gXy94M4
XkT2H9Ielwez5U5xO/ntygzvjO+rJ2kE/mf2ET2i2kptBWxoZiEJ3Nbxv9gKBWhq
DdYDmHP8/oLo0Sm/cm5ocw+24Yvccog4mP6J74WLe6ikFPD+U9GwSWsG9fC+dauS
oeusq1Zc5cApEFYYDimPJSJgCf85VPeEw+BsMnKKslUbIKUPLp2BtyBwJ/bME6iv
q5Dj76AXfatWKX760toa1M324k+wfzdAgjuhh00WqT24UM9wB1WwwwM/xZAoN9mc
WvABHFuLGluPD643XqPN5g5y+l1j+zCvAGK7hQIDAQABAoH/BwCNtwUEcEDmKgAy
nszx3RQcFZMIY+0jiyNODIPXXcLHfGd/zA8Eyzj7QTsKv0neU0VQdHv6lgZ0F4Tk
DEMN54AjH2P2JArKDvLA3Y0IOxAlKO2XII90ulWDGdHj/SF42EXcCj3YcOSBrZxH
G6eX6EPvH+ZXB/aMNFDIjIt9KeILWtCsM8dLxaN7z+x33CcxCEwBeQyg81NsP1Gq
lnp75pbs0N32uhrlhb//gJtoexQVcs1ibChQPGDCWOQZbDZ/+L4Od2kVxWfpTUPh
XZAyl8zAeXjRQq/hHMB4fbXEmweWSCCBZm08FQu0FOHthM7gF9EgzSHmbTj3pHVK
R0ENAoGBAMLeVsStYWwwkv/vzDjRuXDUCYPBSi6GSEQIz0JyEfWBZnlUvgEDkAJ9
SRBJcpICCNRX/acserXq4ErPlTW5xw5xzxVdSbBgWzMVKyNmePWVdb9HgyQ1F/Qn
Ug1+gbkLSa/hSU4OTj7FyW49TlVnKxfYe5fPG0Uwlaq+33/VrFgnAoGBAP2+iMwG
GU1coLoF0RqBrZ804QxrCSwyNxCOUVqquhgHGCHEHHQxcbPC0mzjCWFKWkgMuVIl
INoYZHlH8pSjHUO4PgZ7FrJBHaww6g2mBtvmTCLPNx+aJGH0WaqaBE0k/9NwW56c
aoCFCUPwNxGNcAYu07azVPFcapY/GPj50w5zAoGAQh3mGr0o/OhOOABIrk6aOKn4
wHdoj/iHtG24xLanWUEaX7hc70MiLXYMwDXrZZbDICjqqznwOKEEkN11ptDttPzw
YjNQuUM4LlDUXiJ6j/iyBsBgwnwxMGnW8TUnFn259q7djFpWOf4ppfmvBlMG0ARn
is5+Vi9x2IkClAEPhKkCgYBk3Q89opL+OHq/Vz6WfcPJTFjE+essgU14LEpUcxcE
JBXInk79NQZQgXnpxJne7ZJTn5Mu/wk/CIEv4JSh1vD0EVG+e8E63D1yTANNp5iE
YtgS4jG0Qy6BLYNTGGPrUnDK2JfixaRkL/3N3rfVJ1bHbmfD8ScrxiOsU6qWlZ/6
1wKBgGACsKQfdFPtiK0n2rGm9C23AhdCwrwFDtO3+X191COBg55Wdvc2mUMFSDrj
6rvp+1KfrLjM1xjqtOuTN3Zi7SqHOcHKS7NbYTig976Q2g9gMfgjuICxIzhE9tIN
598OozfIaHiVPHc+sMJ5yS+pLl0bw6siCDQ6Yz3Xfa0xk10P
-----END RSA PRIVATE KEY-----'''

        # try:
        #     with open(path, 'rb') as f:
        #         self.private_key = RSA.import_key(f.read())
        # except:
        #     self.private_key = '1'
        # finally:
        #     print(self.private_key)
        self.private_key = RSA.import_key(private_key)

    # 生成公私钥函数
    @staticmethod
    def generate_key_pair():
        # 使用RSA算法生成一个新的密钥对
        key_pair = RSA.generate(2048)

        # 获取私钥
        private_key = key_pair.export_key()

        # 获取公钥
        public_key = key_pair.publickey().export_key()

        with open('public.pem', 'wb') as f:
            f.write(public_key)

        with open('../static/pwd/private.pem', 'wb') as f:
            f.write(private_key)

    # 解密函数
    def decode(self, data):
        try:
            private_key_obj = PKCS1_v1_5.new(self.private_key)
            decrypted_data = private_key_obj.decrypt(base64.b64decode(data), None)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(e)
            return ''

class HashFunc:
    @staticmethod
    def md5(message):
        if type(message) != bytes:
            hash_object = hashlib.md5(message.encode())
        else:
            hash_object = hashlib.md5(message)
        hash_value = hash_object.hexdigest()
        return hash_value
    @staticmethod
    def hash256(message):
        if type(message) != bytes:
            hash_object = hashlib.sha256(message.encode())
        else:
            hash_object = hashlib.sha256(message)
        hash_value = hash_object.hexdigest()
        return hash_value

    @staticmethod
    def generate_token(message):
        # 生成随机数
        regular_message = str(message)
        random_number = str(random.randint(1, 10000))
        random_str = str(random.randint(32, 127))

        message = regular_message + random_str + random_number

        sha1_hash = hashlib.sha1(message.encode()).hexdigest()
        return sha1_hash

