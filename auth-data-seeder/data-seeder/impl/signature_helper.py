
import traceback
from dynaconf import Dynaconf
from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption
from jwcrypto import jwk, jws
from cryptography.hazmat.primitives import hashes, serialization
import json
import base64

class SignatureHelper(object):

    def __init__(self, seeder_config: Dynaconf) -> None:
        self.seeder_config = seeder_config
        self.sign_private_key, self.sign_cert, self.ca_chain = SignatureHelper._get_priv_key_cert(seeder_config.datashare.sign_p12_file, 
                                                str(seeder_config.datashare.p12_pwd))
        self.algorithm = 'RS256'
        self.sign_priv_key_jws = SignatureHelper._get_jwk_private_key(self.sign_private_key, str(seeder_config.datashare.p12_pwd))
    
    def sign_data(self, data_to_sign: str) -> str:
        print('Request for Sign Auth Request Data.')
        try:
            jws_object = jws.JWS(data_to_sign.encode('UTF-8'))
            jws_object.add_signature(
                self.sign_priv_key_jws,
                None,
                json.dumps({'alg': self.algorithm,
                            'x5c':[base64.encodebytes(self.sign_cert.public_bytes(encoding=serialization.Encoding.PEM)).decode('UTF-8')]}), 
                json.dumps({'kid': base64.encodebytes(self.sign_cert.fingerprint(hashes.SHA256())).decode('UTF-8')}) 
            )

            jws_signature = jws_object.serialize(compact=True).split('.')
            print('Generation for JWS Signature completed.')
            return jws_signature[0] + '..' + jws_signature[2]
        except:
            exp = traceback.format_exc()
            print('Error Signing Data. Error Message: {}'.format(exp))
            raise Exception('Error Signing Data.')


    @staticmethod
    def _get_priv_key_cert(p12_file_path, p12_file_pass):
       
        print('Reading P12 file. File Path: {}'.format(p12_file_path))
        try: 
            with open(p12_file_path, 'rb') as file:
                pem_bytes = file.read()
                return pkcs12.load_key_and_certificates(pem_bytes, bytes(p12_file_pass, 'utf-8'))
        except:
            exp = traceback.format_exc()
            print('Error Loading P12 file to create objects. Error: {}'.format(exp))
            raise Exception('Error Loading P12 file to create objects.')   

    @staticmethod
    def _get_jwk_private_key(priv_key_obj, key_password):

        key_pwd_bytes = bytes(key_password, 'utf-8')
        priv_key_pem = priv_key_obj.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=BestAvailableEncryption(key_pwd_bytes))
        print('Creating JWK key for JWS signing.')
        return jwk.JWK.from_pem(priv_key_pem, password=key_pwd_bytes)