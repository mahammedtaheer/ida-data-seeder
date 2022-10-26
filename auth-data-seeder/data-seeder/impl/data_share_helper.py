from dynaconf import Dynaconf
import requests
import uuid
from datetime import datetime
from impl.api_auth_token_provider import APIAuthTokenProvider
import json
import tempfile
import os


class DataShareHelper(object):


    def __init__(self, seeder_config: Dynaconf) -> None:
        self.seeder_config = seeder_config
        self.data_share_url = seeder_config.datashare.create_url + '/' + seeder_config.datashare.policy_id + '/' + seeder_config.datashare.partner_id
        api_token = APIAuthTokenProvider(seeder_config)
        self.access_token = api_token.get_auth_token()
        if not self.access_token:
            raise RuntimeError('Not able to get access token from keycloak.')

    def create_ds_request(self, enc_values: dict) -> str:

        cred_id = self.seeder_config.datashare.format_id + str(uuid.uuid4())
        schema_list = []
        schema_list.append(self.seeder_config.datashare.schema_name)
        format_issuer = self.seeder_config.datashare.format_issuer
        timestamp_now = datetime.utcnow()
        ts_str = timestamp_now.strftime(self.seeder_config.datashare.timestamp_format) + timestamp_now.strftime('.%f')[0:4] + 'Z'
        issuer = self.seeder_config.datashare.issuer
        consent = ''
        protected_attribs = list(enc_values.keys())

        datashare_json = {}
        datashare_json['id'] = cred_id
        datashare_json['type'] = schema_list
        datashare_json['issuer'] = format_issuer 
        datashare_json['issuanceDate'] = ts_str
        datashare_json['issuedTo'] = issuer 
        datashare_json['consent'] = consent 
        datashare_json['credentialSubject'] = enc_values 
        datashare_json['protectedAttributes'] = protected_attribs

        temp_file_handle, output_path = tempfile.mkstemp(suffix = '.json', prefix='data-share_')
        with os.fdopen(temp_file_handle, "wb") as temp_file:
            temp_file.write(bytes(json.dumps(datashare_json), 'utf-8'))
            temp_file.flush()
            temp_file.seek(0)
            
        cred_file = {'file': open(output_path,'rb')}
        cus_headers = {'Cookie': 'Authorization=' + self.access_token}
        resp = requests.post(self.data_share_url, files=cred_file, headers=cus_headers)
        
        if resp.status_code == 200:
            resp_json = json.loads(resp.text) 
            print ('Uploading Data to datashare successful. Response Data: ' + str(resp_json))
            internal_url = resp_json['dataShare']['url']
            if self.seeder_config.datashare.replace_external_url is True:
                external_url = internal_url.replace('http://datashare.datashare', self.seeder_config.mosip_env.host_url)
                return external_url
                
            return internal_url
        
        raise Exception('Error Uploading credential to DataShare. Response Code:' + resp.status_code)