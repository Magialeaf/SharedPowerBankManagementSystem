import random

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import hashlib
import base64

class RSAFunc:
    def __init__(self, path='../static/pwd/private.pem'):
        private_key = ''''''

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

