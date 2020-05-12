from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
import gi
gi.require_version('NM', '1.0')
from gi.repository import NM, GLib


def ovpn_import(target: Path):
    for vpn_info in NM.VpnPluginInfo.list_load():
        try:
            return vpn_info.load_editor_plugin().import_(str(target))
        except Exception as e:
            print(f"can't import config: {e}")


def import_config(config: str, private_key: str, certificate: str):
    target_parent = Path(mkdtemp())
    target = target_parent / "eduVPN.ovpn"

    with open(target, mode='w+t') as f:
        f.writelines(config)
        f.writelines(f"\n<key>\n{private_key}\n</key>\n")
        f.writelines(f"\n<cert>\n{certificate}\n</cert>\n")

    connection = ovpn_import(target)
    connection.normalize()
    client = NM.Client.new(None)
    main_loop = GLib.MainLoop()

    def added_cb(client, result, _):
        try:
            client.add_connection_finish(result)
            print("The connection profile has been successfully added to NetworkManager.")
        except Exception as e:
            print("ERROR: failed to add connection: %s\n" % e)
        main_loop.quit()

    client.add_connection_async(connection, True, None, added_cb, None)
    main_loop.run()
    rmtree(target_parent)
