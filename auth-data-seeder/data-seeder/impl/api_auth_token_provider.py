
import json
from dynaconf import Dynaconf
import requests

class APIAuthTokenProvider(object):

    def __init__(self, seeder_config: Dynaconf) -> None:
        self.seeder_config = seeder_config

    
    def get_auth_token(self) -> str:

        req_body = {'grant_type': 'client_credentials', 
                    'client_id': self.seeder_config.key_cloak.user_name, 
                    'client_secret': self.seeder_config.key_cloak.user_secret}
        cus_headers = {'content-type': 'application/x-www-form-urlencoded'}

        resp = requests.post(self.seeder_config.key_cloak.url, headers=cus_headers, data=req_body)
        print('Response Code for Keycloak Token: ' + str(resp.status_code))

        if resp.status_code == 200:
            resp_text = resp.text
            resp_text_json = json.loads(resp_text)
            return resp_text_json['access_token']
        
        return None