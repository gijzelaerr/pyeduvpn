from pathlib import Path
from requests_oauthlib import OAuth2Session
from pyeduvpn.menu import menu, profile_choice, write_to_nm_choice
from pyeduvpn.nm import save_connection, write_config
from pyeduvpn.oauth2 import get_oauth
from pyeduvpn.remote import get_info, list_profiles, get_config, create_keypair
from pyeduvpn.settings import CLIENT_ID
from pyeduvpn.storage import get_entry, set_entry


def main():
    base_url = menu()

    exists = get_entry(base_url)

    if exists:
        token, api_base_uri, token_endpoint, authorization_endpoint = exists
        oauth = OAuth2Session(client_id=CLIENT_ID, token=token, auto_refresh_url=token_endpoint)
    else:
        api_base_uri, token_endpoint, auth_endpoint = get_info(base_url)
        oauth = get_oauth(token_endpoint, auth_endpoint)
        set_entry(base_url, oauth.token, api_base_uri, token_endpoint, auth_endpoint)

    oauth.refresh_token(token_url=token_endpoint)

    profiles = list_profiles(oauth, api_base_uri)
    profile_id = profile_choice(profiles)
    config = get_config(oauth, api_base_uri, profile_id)
    private_key, certificate = create_keypair(oauth, api_base_uri)

    if write_to_nm_choice():
        save_connection(config, private_key, certificate)
    else:
        target = Path('eduVPN.ovpn').resolve()
        print(f"Writing configuration to {target}")
        write_config(config, private_key, certificate, target)


if __name__ == '__main__':
    main()
