
from generator.random_generator import RandomGenerator
from dynaconf import Dynaconf
from pathlib import Path
import csv

class SecretGenerator:

    def __init__(self, seeder_config: Dynaconf):
        self.seeder_config = seeder_config
    
    def generate_required_secrets(self):
        print ('Generating Require number of salts.')
                
        """ rand_gen = RandomGenerator(self.seeder_config.random_generator.salt_file_store, 
                                   self.seeder_config.random_generator.salt_start_index, 
                                   self.seeder_config.random_generator.salt_max_index, 
                                   self.seeder_config.random_generator.salt_bytes_size)

        rand_gen.generate_random_secrect_and_store() """

        file_path = Path(self.seeder_config.random_generator.salt_file_store)
        if (file_path.is_file()):
            print ('File Exists, Checking for salts in the file.')
            with open(file_path, 'r+') as file_obj:
                csv_reader = csv.reader(file_obj)
                no_of_lines = len(list(csv_reader))
                print ('Number of salts available in file: ' + str(no_of_lines))
                if no_of_lines < 1000:
                    print ('Required number of salts not available.')
                    print ('Export "idrepo.uin_hash_salt" table from the DB into an CSV file.')
                    print ('Note: Select only two columns from the table. Columns are "id", "salt"')
                    print ('Output Eg: "1,upcNyMqhkDwJhFJg18vRmg=="')
                    raise RuntimeError('Required number of salts are not available.')

        print ('Require Number of Salts are available in the file.')

        print ('Generating Require number of ZK Keys.')
                
        rand_gen = RandomGenerator(self.seeder_config.random_generator.zk_keys_file_store, 
                                   self.seeder_config.random_generator.zk_keys_start_index, 
                                   self.seeder_config.random_generator.zk_keys_max_index, 
                                   self.seeder_config.random_generator.zk_key_bytes_size)

        rand_gen.generate_random_secrect_and_store()
        print ('ZK Keys Generation Completed.')

        