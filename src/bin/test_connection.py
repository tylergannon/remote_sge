import argparse
from os.path import exists, join, abspath
import requests

class NotFound(Exception):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configdir', help="The location of the configs")
    args = parser.parse_args()

    configdir = abspath(args.configdir)
    if not exists(configdir):
        raise NotFound("Couldn't find configdir you gave.")
    
    key = join(configdir, 'certs', 'client.key')
    cert = join(configdir, 'certs', 'client.crt')

    response = requests.get("https://localhost/", cert=(cert, key), verify=False)
    if response.status_code == 200:
        print("It works!")
    else:
        print("Responded with %s" % response.status_code)
        print("Response body: " + response.text)

if __name__ == '__main__':
    main()
