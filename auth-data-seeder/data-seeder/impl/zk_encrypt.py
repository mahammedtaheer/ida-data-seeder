
from typing import List
from impl.crypto_data_provider import CryptoDataProvider
from model.auth_data import DemographicsModel
import random
from dynaconf import Dynaconf
from impl.hash_generator import IdHashGenerator
import base64
import os
from cryptography import x509
from cryptography.hazmat.primitives import hashes, asymmetric, ciphers
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import Certificate

class ZKEncryptor(object):

    def __init__(self, crypto_data_provider: CryptoDataProvider, seeder_config: Dynaconf, id_hash_gen: IdHashGenerator, **kwargs):
        self.crypto_data_provider = crypto_data_provider
        self.seeder_config = seeder_config
        self.id_hash_gen = id_hash_gen
        self.asymmetric_encrypt_padding = padding.OAEP(
                                                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),
                                                label=None)
        self.cert_obj = ZKEncryptor._get_cert_obj(seeder_config.ida.public_key)


    def zk_encrypt(self, input_data: DemographicsModel) -> dict:

        rand_index = random.randint(1, self.seeder_config.random_generator.zk_keys_max_index)
        random_key = self.crypto_data_provider.get_zk_key(str(rand_index))
        id = input_data.id
        derived_key = self._get_derived_key(id, random_key)

        enc_values = {}
        enc_values['fullName'] = self._encrypt_data(derived_key, self._get_str(input_data.name), rand_index)
        enc_values['gender'] = self._encrypt_data(derived_key, self._get_str(input_data.gender), rand_index)
        enc_values['dateOfBirth'] = self._encrypt_data(derived_key, input_data.dob, rand_index)
        enc_values['phone'] = self._encrypt_data(derived_key, input_data.phoneNumber, rand_index)
        enc_values['email'] = self._encrypt_data(derived_key, input_data.emailId, rand_index)
        enc_values['addressLine1'] = self._encrypt_data(derived_key, self._get_str(input_data.addressLine1), rand_index)
        enc_values['addressLine2'] = self._encrypt_data(derived_key, self._get_str(input_data.addressLine2), rand_index)
        enc_values['addressLine3'] = self._encrypt_data(derived_key, self._get_str(input_data.addressLine3), rand_index)
        enc_values['city'] = self._encrypt_data(derived_key, self._get_str(input_data.city), rand_index)
        enc_values['postalCode'] = self._encrypt_data(derived_key, input_data.postalCode, rand_index)
        enc_values['province'] = self._encrypt_data(derived_key, self._get_str(input_data.province), rand_index)
        enc_values['region'] = self._encrypt_data(derived_key, self._get_str(input_data.region), rand_index)
        enc_values['zone'] = self._encrypt_data(derived_key, self._get_str(input_data.zone), rand_index)
        
        enc_random_key = self._enc_random_key(random_key)
        return enc_values, enc_random_key
        

    def _get_derived_key(self, id: str, random_key: str) -> bytes:
        id_hash = bytes.fromhex(self.id_hash_gen.generate_id_plain_hash(id))
        random_key_bytes = base64.b64decode(random_key)
        aes_encryptor_obj = ciphers.Cipher(ciphers.algorithms.AES(random_key_bytes), ciphers.modes.ECB()).encryptor()

        derived_key = aes_encryptor_obj.update(id_hash) + aes_encryptor_obj.finalize()
        return derived_key

    
    def _encrypt_data(self, derived_key: bytes, data_to_enc: str, rand_index: int) -> str:

        aad = os.urandom(32)
        nonce = os.urandom(12)
        data_to_enc_bytes = bytes(data_to_enc, 'utf-8')
        aes_encryptor_obj = ciphers.Cipher(ciphers.algorithms.AES(derived_key),
                                   ciphers.modes.GCM(nonce, tag=None, min_tag_length=12)).encryptor()
        aes_encryptor_obj.authenticate_additional_data(aad)
        enc_data = aes_encryptor_obj.update(data_to_enc_bytes) + aes_encryptor_obj.finalize()
        enc_data_tag = enc_data + aes_encryptor_obj.tag
        enc_data_concat = bytes(str(rand_index), 'utf-8') + nonce + aad + enc_data_tag
        return base64.urlsafe_b64encode(enc_data_concat).decode('utf-8')


    def _get_str(self, data_to_enc: list) -> List:
        ret_value = []
        for data in data_to_enc:
            ret_value.append(str(data.dict()))
        
        return str(ret_value)

    def _enc_random_key(self, random_key:str ) -> str:
        pub_key_obj = self.cert_obj.public_key()
        return pub_key_obj.encrypt(base64.b64decode(random_key), self.asymmetric_encrypt_padding)

    def _get_cert_obj(cert_path: str) -> Certificate:
        with open(cert_path, 'rb') as file:
            cert = x509.load_pem_x509_certificate(file.read())
            return cert