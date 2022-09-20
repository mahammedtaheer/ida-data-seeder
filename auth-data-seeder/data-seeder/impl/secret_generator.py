
from generator.random_generator import RandomGenerator
from dynaconf import Dynaconf

class SecretGenerator:

    def __init__(self, seeder_config: Dynaconf):
        self.seeder_config = seeder_config
    
    def generate_required_secrets(self):
        print ('Generating Require number of salts.')
                
        rand_gen = RandomGenerator(self.seeder_config.random_generator.salt_file_store, 
                                   self.seeder_config.random_generator.salt_max_index, 
                                   self.seeder_config.random_generator.salt_bytes_size)

        rand_gen.generate_random_secrect_and_store()
        print ('Salt Generation Completed.')

        print ('Generating Require number of ZK Keys.')
                
        rand_gen = RandomGenerator(self.seeder_config.random_generator.zk_keys_file_store, 
                                   self.seeder_config.random_generator.zk_keys_max_index, 
                                   self.seeder_config.random_generator.zk_key_bytes_size)

        rand_gen.generate_random_secrect_and_store()
        print ('ZK Keys Generation Completed.')

        