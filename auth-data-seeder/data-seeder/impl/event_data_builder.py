
from urllib import request
from dynaconf import Dynaconf
import uuid
from datetime import datetime, timedelta
import json

class EventDataBuilder(object):


    def __init__(self, seeder_config: Dynaconf) -> None:
        self.seeder_config = seeder_config

    def build_event_data(self, enc_key: str, rand_index: int, signed_data: str, data_share_url: str, 
                        vid_hash: str, salt_index: str, salt_data: str, plain_hash: str) -> str:
        data_dict = {}
        data_dict['demoEncryptedRandomKey'] = enc_key
        data_dict['demoRankomKeyIndex'] = str(rand_index)
        data_dict['credentialType'] = 'auth'
        data_dict['protectionKey'] = None
        proof_dict = {}
        proof_dict['signature'] = signed_data
        data_dict['MODULO'] = salt_index
        data_dict['SALT'] = salt_data
        data_dict['TOKEN'] = plain_hash
        data_dict['id_hash'] = vid_hash
        data_dict['transaction_limit'] = 5
        timestamp_now = datetime.utcnow() + timedelta(days=180)
        exp_ts_str = timestamp_now.strftime(self.seeder_config.datashare.timestamp_format) + timestamp_now.strftime('.%f')[0:4] + 'Z'
        data_dict['expiry_timestamp'] = exp_ts_str
        data_dict['proof'] = proof_dict

        event_data_dict = {}
        event_data_dict['data'] = data_dict
        event_data_dict['dataShareUri'] = data_share_url
        event_data_dict['id'] = EventDataBuilder._gen_uuid()
        timestamp_now = datetime.utcnow()
        ts_str = timestamp_now.strftime(self.seeder_config.datashare.timestamp_format) + timestamp_now.strftime('.%f')[0:4] + 'Z'
        event_data_dict['timestamp'] = ts_str
        event_data_dict['transactionId'] = EventDataBuilder._gen_uuid()
        event_data_dict['type'] = {'name': 'mosip', 'namespace': 'mosip'}

        final_dict = {}
        final_dict['event'] = event_data_dict
        final_dict['publishedOn'] = ts_str
        final_dict['publisher'] = self.seeder_config.mosip_websub.publisher
        final_dict['topic'] = self.seeder_config.mosip_websub.topic

        return json.dumps(final_dict)

    @staticmethod
    def _gen_uuid() -> str:
        return str(uuid.uuid4())

