from typing import Union, Dict
import requests
from requests_oauthlib import OAuth2Session
from pyeduvpn.crypto import common_name_from_cert
from pyeduvpn.settings import ORGANISATION_URI, COUNTRY, LANGUAGE, INSTITUTES_URI


def list_orgs():
    org_list_response = requests.get(ORGANISATION_URI)
    organization_list = org_list_response.json()['organization_list']
    return organization_list


def extract_translation(d: Union[str, Dict[str, str]]):
    if type(d) != dict:
        return d
    for m in [COUNTRY, LANGUAGE, 'en-US', 'en']:
        try:
            return d[m]
        except KeyError:
            continue
    return list(d.values())[0]  # otherwise just return first in list


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


def list_institutes():
    institute_access_response = requests.get(INSTITUTES_URI)
    institute_access_list = institute_access_response.json()['instances']
    return institute_access_list
