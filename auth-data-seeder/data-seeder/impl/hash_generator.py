
from cryptography.hazmat.primitives import hashes
from .crypto_data_provider import CryptoDataProvider
import base64
from dynaconf import Dynaconf

class IdHashGenerator(object):

    def __init__(self, crypto_data_provider: CryptoDataProvider, seeder_config: Dynaconf):
        self.crypto_data_provider = crypto_data_provider
        self.seeder_config = seeder_config


    def generate_id_hash(self, input_id: str) -> str:
        if self.seeder_config.ida.is_ida_ver_115:
            decimal_index_value = input_id[-3:]
        else: 
            sha256_hash_obj = hashes.Hash(hashes.SHA256())
            sha256_hash_obj.update(bytes(input_id, 'utf-8'))
            id_data_hash = sha256_hash_obj.finalize().hex().upper()

            hex_index_value = IdHashGenerator.get_index_value(id_data_hash, 16)
            decimal_index_value = IdHashGenerator.get_index_value(hex_index_value, 10)

        salt_data = self.crypto_data_provider.get_salt_crypto_data(decimal_index_value)

        sha256_hash_obj = hashes.Hash(hashes.SHA256())
        sha256_hash_obj.update(bytes(input_id, 'utf-8'))
        sha256_hash_obj.update(bytes(salt_data, 'utf-8'))
        return sha256_hash_obj.finalize().hex().upper(), decimal_index_value, salt_data


    def generate_id_plain_hash(self, input_id: str) -> str:
        sha256_hash_obj = hashes.Hash(hashes.SHA256())
        sha256_hash_obj.update(bytes(input_id, 'utf-8'))
        return sha256_hash_obj.finalize().hex().upper()

    @staticmethod
    def get_index_value(input_data: str, radix: int):
        input_data_len = len(input_data)
        input_data_substr = input_data[-3:] if (input_data_len > 3) else input_data
        return str(int(input_data_substr, radix))
        