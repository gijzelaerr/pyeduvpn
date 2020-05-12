from typing import Optional, Tuple
import json
from pathlib import Path
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token
from pyeduvpn.settings import CONFIG_PREFIX
from pyeduvpn.type import url
from pyeduvpn.utils import get_logger

logger = get_logger(__name__)
metadata_path = CONFIG_PREFIX / "metadata"


def read_storage() -> dict:
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(e)
    return {}


def write_storage(storage: dict) -> None:
    try:
        with open(metadata_path, 'w') as f:
            return json.dump(storage, fp=f)
    except Exception as e:
        logger.error(e)


def get_entry(base_url: str) -> Optional[Tuple[OAuth2Token, url, url, url]]:
    storage = read_storage()
    if base_url in storage:
        v = storage[base_url]
        return OAuth2Token(v['token']), v['api_base_uri'], v['token_endpoint'], v['authorization_endpoint']


def set_entry(base_url: str,
              token: OAuth2Token,
              api_base_uri: url,
              token_endpoint: url,
              authorization_endpoint: url,

              ) -> None:
    storage = read_storage()
    storage[base_url] = {
        'token': token,
        'api_base_uri': api_base_uri,
        'token_endpoint': token_endpoint,
        'authorization_endpoint': authorization_endpoint,
    }
    write_storage(storage)


def get_eduvpn_uuid() -> Optional[str]:
    p = Path("~/.config/eduvpn/uuid").expanduser()
    if p.exists():
        return open(p, 'r').read()
    else:
        return None


def set_eduvpn_uuid(uuid: str):
    p = Path("~/.config/eduvpn/uuid").expanduser()
    with open(p, 'w') as f:
        f.write(uuid)


def clear_eduvpn_uuid():
    p = Path("~/.config/eduvpn/uuid").expanduser()
    p.unlink(missing_ok=True)
