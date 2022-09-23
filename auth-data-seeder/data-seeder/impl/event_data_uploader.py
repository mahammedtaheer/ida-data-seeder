
from dynaconf import Dynaconf
from cryptography.hazmat.primitives import hashes
import requests
import hmac
import hashlib

class EventDataUploader(object):

    def __init__(self, seeder_config: Dynaconf) -> None:
        self.seeder_config = seeder_config
        
    
    def post_event_data(self, event_data: str) -> None:

        cus_header = {'accept': 'application/json',
                      'Content-type': 'application/json',
                      'x-hub-signature': self._build_header(event_data)}
        cred_service_url = self.seeder_config.ida.cred_service_url + self.seeder_config.datashare.partner_id
        resp = requests.post(cred_service_url, data=event_data, headers=cus_header)
        print (resp.status_code)
        print (resp.text)
        

    def _build_header(self, event_data:str) -> str:
        
        secret_bytes = bytes(self.seeder_config.ida.websub_secret, 'utf-8')
        event_data_bytes = bytes(event_data.replace('\'', '"'), 'utf-8')

        digest_bytes = hmac.new(secret_bytes, msg=event_data_bytes, digestmod=hashlib.sha256).digest()
        return 'SHA256=' + digest_bytes.hex().lower()
