from typing import Optional
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
import gi

gi.require_version('NM', '1.0')
from gi.repository import NM, GLib
from pyeduvpn.storage import set_eduvpn_uuid, get_eduvpn_uuid
from pyeduvpn.utils import get_logger

logger = get_logger(__file__)


def ovpn_import(target: str) -> Optional[NM.Connection]:
    for vpn_info in NM.VpnPluginInfo.list_load():
        try:
            return vpn_info.load_editor_plugin().import_(str(target))
        except Exception as e:
            continue
    return None


def import_ovpn(config: str, private_key: str, certificate: str) -> NM.Connection:
    target_parent = Path(mkdtemp())
    target = target_parent / "eduVPN.ovpn"

    with open(target, mode='w+t') as f:
        f.writelines(config)
        f.writelines(f"\n<key>\n{private_key}\n</key>\n")
        f.writelines(f"\n<cert>\n{certificate}\n</cert>\n")

    connection = ovpn_import(target)
    # Does some basic normalization and fixup of well known inconsistencies
    # and deprecated fields. If the connection was modified in any way,
    # the output parameter modified is set TRUE.
    connection.normalize()
    rmtree(target_parent)
    return connection


def add_connection(client: NM.Client, connection: NM.Connection, main_loop: GLib.MainLoop):
    def add_callback(client, result, data):
        try:
            new_con = client.add_connection_finish(result)
            set_eduvpn_uuid(uuid=new_con.get_uuid())
        except Exception as e:
            logger.error("ERROR: failed to add connection: %s\n" % e)
        main_loop.quit()

    client.add_connection_async(connection=connection, save_to_disk=True, cancellable=None,
                                callback=add_callback, user_data=None)


def update_connection(old_con: NM.Connection, new_con: NM.Connection, main_loop: GLib.MainLoop):
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
        logger.info("updating existing")
        old_con = client.get_connection_by_uuid(uuid)
        update_connection(old_con, new_con, main_loop)
    else:
        logger.info("adding new")
        add_connection(client=client, connection=new_con, main_loop=main_loop)
    main_loop.run()
