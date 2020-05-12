from typing import Tuple
from pathlib import Path
from pyeduvpn.utils import get_prefix

prefix = get_prefix()

CONFIG_PREFIX = Path("~/.config/eduvpn/").expanduser().resolve()

INSTITUTES_URI = "https://static.eduvpn.nl/disco/institute_access.json"
DISCO_URI = 'https://disco.eduvpn.org/'
ORGANISATION_URI = DISCO_URI + "organization_list_2.json"
CLIENT_ID = "org.eduvpn.app.linux"
SCOPE = ["config"]
CODE_CHALLENGE_METHOD = "S256"
LANGUAGE = 'nl'
COUNTRY = "nl-NL"
eduvpn_main_logo = prefix + "/share/icons/hicolor/128x128/apps/eduvpn-client.png"
eduvpn_name = "eduVPN"
lets_connect_main_logo = prefix + "/share/icons/hicolor/128x128/apps/lets-connect-client.png"
lets_connect_name = "Let's Connect!"


def get_brand(lets_connect: bool) -> Tuple[str, str]:
    """
    args:
        lets_connect: Set true if we are let's connect, otherwise eduVPN
    returns:
        logo, name
    """
    if lets_connect:
        return lets_connect_main_logo, lets_connect_name
    else:
        return eduvpn_main_logo, eduvpn_name
