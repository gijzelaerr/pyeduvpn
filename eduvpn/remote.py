import requests
import logging
from base64 import b64decode
from requests_oauthlib import OAuth2Session
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from eduvpn.crypto import common_name_from_cert
from eduvpn.type import url

logger = logging.getLogger(__name__)


def list_orgs(uri: url, verifier: Ed25519PublicKey):
    logger.info(u"Discovering organisations at {}".format(uri))
    response = requests.get(uri)
    if response.status_code != 200:
        msg = "Got error code {} requesting {}".format(response.status_code, uri)
        logger.error(msg)
        raise IOError(msg)
    sig_uri = uri + '.minisig'
    logger.info(u"Retrieving signature {}".format(sig_uri))
    sig_response = requests.get(sig_uri)
    if sig_response.status_code != 200:
        msg = "Can't retrieve signature, requesting {} gave error code {}".format(sig_uri, sig_response.status_code)
        logger.warning(msg)
    else:
        logger.info(u"verifying signature of {}".format(sig_response))
        signature = sig_response.content.decode('utf-8').split("\n")[1]
        decoded = b64decode(signature)[10:]
        _ = verifier.verify(data=response.content, signature=decoded)
    organization_list = response.json()['organization_list']
    return organization_list


def get_info(base_uri: str):
    info_url = base_uri + 'info.json'
    info = requests.get(info_url).json()['api']['http://eduvpn.org/api#2']
    api_base_uri = info['api_base_uri']
    token_endpoint = info['token_endpoint']
    auth_endpoint = info['authorization_endpoint']
    return api_base_uri, token_endpoint, auth_endpoint


def get_config(oauth, api_base_uri, profile_id):
    response = oauth.get(api_base_uri + f'/profile_config?profile_id={profile_id}')
    return response.text


def list_profiles(oauth, api_base_uri):
    profile_list_response = oauth.get(api_base_uri + '/profile_list')
    return profile_list_response.json()['profile_list']['data']


def create_keypair(oauth: OAuth2Session, api_base_uri: str) -> (str, str):
    response = oauth.post(api_base_uri + '/create_keypair')
    keypair = response.json()['create_keypair']['data']
    private_key = keypair['private_key']
    certificate = keypair['certificate']
    return private_key, certificate


def system_messages(oauth: OAuth2Session, api_base_uri: str):
    response = oauth.get(api_base_uri + '/system_messages')
    return response.json()['system_messages']['data']


def check_certificate(oauth: OAuth2Session, api_base_uri: str, certificate: str):
    common_name = common_name_from_cert(certificate.encode('ascii'))
    response = oauth.get(api_base_uri + '/check_certificate?common_name=' + common_name)
    return response.json()['check_certificate']['data']['is_valid']


def list_institutes(uri: str, verifier: Ed25519PublicKey):
    response = requests.get(uri)
    institute_access_list = response.json()['instances']
    return institute_access_list
