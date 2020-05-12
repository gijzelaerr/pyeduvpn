import webbrowser
from requests_oauthlib import OAuth2Session
from pyeduvpn.menu import menu
from pyeduvpn.nm import import_config
from pyeduvpn.crypto import gen_code_verifier, gen_code_challenge
from pyeduvpn.oauth2 import get_open_port, one_request, get_oauth
from pyeduvpn.remote import extract_translation, list_orgs, get_info, list_profiles, get_config, create_keypair, \
    extract_translation, list_orgs
from pyeduvpn.settings import CLIENT_ID, SCOPE, CODE_CHALLENGE_METHOD, INSTITUTES_URI
from pyeduvpn.storage import get_entry, set_entry
from pyeduvpn.type import url


def fetch_new_token(port: int, redirect_uri: url, token_endpoint: url, authorization_endpoint: url):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=redirect_uri, auto_refresh_url=token_endpoint, scope=scope)
    code_verifier = gen_code_verifier()
    code_challenge = gen_code_challenge(code_verifier)
    authorization_url, state = oauth.authorization_url(url=authorization_endpoint,
                                                       code_challenge_method=CODE_CHALLENGE_METHOD,
                                                       code_challenge=code_challenge)
    webbrowser.open(authorization_url)
    response = one_request(port, lets_connect=False)
    code = response['code'][0]
    assert (state == response['state'][0])
    token = oauth.fetch_token(token_url=token_endpoint,
                              code=code,
                              code_verifier=code_verifier,
                              client_id=oauth.client_id,
                              include_client_id=True,
                              )
    return oauth


def main():
    base_url = menu()

    exists = get_entry(base_url)

    if exists:
        token, api_base_uri, token_endpoint, authorization_endpoint = exists
        oauth = OAuth2Session(client_id=CLIENT_ID, token=token, auto_refresh_url=token_endpoint)
    else:
        api_base_uri, token_endpoint, auth_endpoint = get_info(base_url)
        oauth = fetch_new_token(redirect_uri, token_endpoint)
        set_entry(base_url, oauth.token, api_base_uri, token_endpoint, auth_endpoint)

    api_base_uri, token_endpoint, auth_endpoint = get_info(base_url)
    oauth = get_oauth(token_endpoint, auth_endpoint)
    profile_id = list_profiles(oauth, api_base_uri)[0]['profile_id']
    config = get_config(oauth, api_base_uri, profile_id)
    private_key, certificate = create_keypair(oauth, api_base_uri)
    import_config(config, private_key, certificate)
