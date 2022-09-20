import os
import json
from dynaconf import Dynaconf
from impl.secret_generator import SecretGenerator
from impl.input_data_provider import SeedDataReader
from impl.crypto_data_provider import CryptoDataProvider
from impl.hash_generator import IdHashGenerator
from impl.zk_encrypt import ZKEncryptor
from impl.data_share_helper import DataShareHelper
from stdnum import verhoeff


ida_seeder_config = Dynaconf(settings_files=[os.path.join(os.path.dirname(__file__),'config/config.toml')])

if __name__ == "__main__":
    
    print ('Started IDA Data Seeder...')
    print ('\nConfigure Environment for data feed: ' + ida_seeder_config.mosip_env.host_url)

    secret_gen = SecretGenerator(ida_seeder_config)
    secret_gen.generate_required_secrets()

    print ('Creating Crypto Data Reader Object.')
    crypto_data_provider = CryptoDataProvider(ida_seeder_config)

    print ('Creating Id Hash Generator Object.')
    id_hash_gen = IdHashGenerator(crypto_data_provider)

    seed_data_reader = SeedDataReader(ida_seeder_config)
    input_data_list = seed_data_reader.read_and_parse_data()
    print ('Total Number of Records found: ' + str(len(input_data_list)))

    zk_encrypt = ZKEncryptor(crypto_data_provider, ida_seeder_config, id_hash_gen)
    ds_helpher = DataShareHelper(ida_seeder_config)
    for input_data in input_data_list:
        id = input_data.id
        vid_hash, salt_index = id_hash_gen.generate_id_hash(id)
        plain_hash = id_hash_gen.generate_id_plain_hash(id)
        enc_data, enc_key = zk_encrypt.zk_encrypt(input_data)
        ds_helpher.create_ds_request(enc_data)


