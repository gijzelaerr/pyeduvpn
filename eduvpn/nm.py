from logging import getLogger
from typing import Optional
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

logger = getLogger(__name__)

try:
    import gi
    gi.require_version('NM', '1.0')
    from gi.repository import NM, GLib
except (ImportError, ValueError) as e:
    logger.warning("Network Manager not available")
    NM = GLib = None

from eduvpn.storage import set_eduvpn_uuid, get_eduvpn_uuid, write_config
from eduvpn.utils import get_logger

logger = get_logger(__file__)


def nm_available() -> bool:
    """
    check if Network Manager is available
    """
    return bool(NM)


def ovpn_import(target: str) -> Optional['NM.Connection']:
    """
    Use the Network Manager VPN config importer to import an OpenVPN configuration file.
    """
    for vpn_info in NM.VpnPluginInfo.list_load():
        try:
            return vpn_info.load_editor_plugin().import_(str(target))
        except Exception as e:
            continue
    return None


def import_ovpn(config: str, private_key: str, certificate: str) -> 'NM.Connection':
    """
    Import the OVPN string into Network Manager.
    """
    target_parent = Path(mkdtemp())
    target = target_parent / "eduVPN.ovpn"
    write_config(config, private_key, certificate, target)
    connection = ovpn_import(target)
    connection.normalize()
    rmtree(target_parent)
    return connection


def add_connection(client: 'NM.Client', connection: 'NM.Connection', main_loop: 'GLib.MainLoop'):
    logger.info("Adding new connection")
    def add_callback(client, result, data):
        try:
            new_con = client.add_connection_finish(result)
            set_eduvpn_uuid(uuid=new_con.get_uuid())
        except Exception as e:
            logger.error("ERROR: failed to add connection: %s\n" % e)
        main_loop.quit()

    client.add_connection_async(connection=connection, save_to_disk=True, cancellable=None,
                                callback=add_callback, user_data=None)


def update_connection(old_con: 'NM.Connection', new_con: 'NM.Connection', main_loop: 'GLib.MainLoop'):
    """
    Update an existing Network Manager connection with the settings from another Network Manager connection
    """
    logger.info("Updating existing connection with new configuration")
    def update_callback(client, result, data):
        main_loop.quit()

    old_con.replace_settings_from_connection(new_con)
    old_con.commit_changes_async(save_to_disk=True, cancellable=None, callback=update_callback, user_data=None)


def save_connection(config, private_key, certificate):
    new_con = import_ovpn(config, private_key, certificate)
    uuid = get_eduvpn_uuid()
    main_loop = GLib.MainLoop()
    client = NM.Client.new()
    if uuid:
        old_con = client.get_connection_by_uuid(uuid)
        if old_con:
            update_connection(old_con, new_con, main_loop)
        else:
            add_connection(client=client, connection=new_con, main_loop=main_loop)
    else:
        add_connection(client=client, connection=new_con, main_loop=main_loop)
    main_loop.run()
