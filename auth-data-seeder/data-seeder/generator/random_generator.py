from inspect import _void
from zope.interface import  Interface, Attribute, implementer
import secrets
from pathlib import Path
import base64

class RandomGenerator(object):
    
    def __init__(self, file_path: str, start_index_number: int, max_index_number: int, bytes_size: int):
        self.store_file_path = file_path
        self.start_index_number = start_index_number
        self.max_index_number = max_index_number
        self.bytes_size = bytes_size

    def generate_random_secrect_and_store(self):
        file_path = Path(self.store_file_path)
        if (file_path.is_file()):
            print ('File Exists, Ramdom might have generated.')
            return

        print ('Generating Random bytes for max index: ' + str(self.max_index_number))
        data_dict = {}
        for i in range(self.start_index_number, self.max_index_number):
            data_dict[i] = self._generator_random_bytes()

        self._store_data(data_dict)
        print ('Random Generation Successful and store in inpur path: ' + str(self.store_file_path))

    def _generator_random_bytes(self) -> str:
        return base64.b64encode(secrets.token_bytes(self.bytes_size)).decode('utf-8')

    def _store_data(self, data_dict: dict):

        with open(self.store_file_path, 'w+') as store:
            for key, value in data_dict.items():
                print (str(key) + ',' + value, file=store)
            store.flush()