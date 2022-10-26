
import csv
from dynaconf import Dynaconf

class CryptoDataProvider(object):

    def __init__(self, seeder_config: Dynaconf) :
        self.salt_crypto_data = CryptoDataProvider._read_files(seeder_config.random_generator.salt_file_store)
        self.zk_keys_data = CryptoDataProvider._read_files(seeder_config.random_generator.zk_keys_file_store)
        

    @staticmethod
    def _read_files(file_path: str):

        crypto_data = {}
        with open(file_path, 'r+') as file_obj:
            csv_reader = csv.reader(file_obj)

            for file_line in csv_reader:
                crypto_data[file_line[0]] = file_line[1]  
        
        return crypto_data

    def get_salt_crypto_data(self, index: int):
        return self.salt_crypto_data.get(index, None)

    def get_zk_key(self, index: int):
        return self.zk_keys_data.get(index, None)
    
