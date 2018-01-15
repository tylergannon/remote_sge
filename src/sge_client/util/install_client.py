"""
Client installer
"""

import os
from os.path import join, expandvars
import tarfile
import argparse
from sge_server.util.install_server import (EDITOR_TEXT, ROOT_DESCRIPTION, get_editor,
                                            edit_config_file, maybe_sudo, sudo)

parser = argparse.ArgumentParser(prog="remote_sge install_client",
                                 formatter_class=argparse.RawTextHelpFormatter)


END_MESSAGE = """
Installation is complete.  The certificates have been placed in %s. Please verify
permissions on the certificate files, and consider deleting the copy of your keys
at %s.

Use "remote_sge shuttle" to move jobs to the remote server.  Thanks for playing the game!
"""

def do_install():
    args = parse_args()
    editor = args.editor
    certs_location = join(args.root, "certs")
    maybe_sudo("mkdir -p " + certs_location)
    maybe_sudo("tar zxfp %s -C %s" % (args.certificates, certs_location))
    edit_config_file("Config file", "config.ini", args.root, editor=editor)
    print(END_MESSAGE % (certs_location, args.certificates))

def parse_args():
    parser.add_argument("install_client", help="The name of this command")
    parser.add_argument('-i', '--install',
                        help="Perform the installation.",
                        action="store_true")
    parser.add_argument('-c', '--certificates',
                        help=("Location of tarfile archive containing certificates.  " +
                              "Defaults to $HOME/remote_sge_client_certs.tgz"),
                        default=expandvars("$HOME/remote_sge_client_certs.tgz"))
    parser.add_argument('-e', '--editor',
                        help=EDITOR_TEXT, default='vim')
    parser.add_argument('-r', '--root',
                        help=ROOT_DESCRIPTION,
                        default="$HOME/.config/remote_sge")
    parser.add_argument('-s', '--sudo',
                        help="Use sudo for placing config files (e.g. if installing into /etc).",
                        action="store_true")
    return parser.parse_args()
