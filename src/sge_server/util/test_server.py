from os.path import exists, join, abspath, expanduser, expandvars
import requests
from sge.util.arg_parser import ArgParser

class NotFound(Exception):
    pass

CONFIGDIR_HELP = """The location of the config files.  Probably either ~/.config/remote_sge,
or /etc/remote_sge."""

def main():
    parser = ArgParser(prog="remote_sge")
    parser.add_argument('test_server', help="Command to run")
    parser.add_argument('configdir', help=CONFIGDIR_HELP)
    parser.add_argument('-H', '--host', help="Hostname.  Default: localhost", default="localhost")
    parser.add_argument('-p', '--port', help="Port to connect to.  Default: 443", default="443")
    parser.add_argument('-s', '--socket', help="Path to Unix domain socket to connect to.  Default: None." +
                        " If supplied, -h and -p are ignored and unix domain socket will be " +
                        "connected to rather than a TCP connection.  Requires the " +
                        "requests-unixsocket package which must be installed manually.")
    parser.add_argument('-k', '--key',
                        help="Path to client private key.  Default is $configdir/certs/client.key",
                        default=None)
    parser.add_argument('-c', '--cert',
                        help="Path to client certificate.  Default is $configdir/certs/client.crt",
                        default=None)

    args = parser.parse_args()

    configdir = abspath(expandvars(expanduser(args.configdir)))
    if not exists(configdir):
        raise NotFound("Couldn't find configdir you gave.")

    if args.key:
        key = args.key
    else:
        key = join(configdir, 'certs', 'client.key')

    if args.cert:
        cert = args.cert
    else:
        cert = join(configdir, 'certs', 'client.crt')

    if args.socket:
        import requests_unixsocket
        from urllib.parse import urlencode
        requests_unixsocket.monkeypatch()
        response = requests.get("http+unix://%s/" % urlencode(args.socket))
    else:
        params = dict(cert=(cert, key), verify=False)
        response = requests.get("https://%s:%s/" % (args.host, args.port), **params)
    if response.status_code == 200:
        print("It works!")
    else:
        print("Responded with %s" % response.status_code)
        print("Response body: " + response.text)

if __name__ == '__main__':
    main()
