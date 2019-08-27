#!/usr/bin/env python
"""
Usage:
    teslacli.py [options] <action>

Options:
    -c, --config-file CONFIG_FILE
    -h, --help                      Display this dialog

"""
from __future__ import absolute_import, print_function

import os
import sys
from pprint import pprint

import yaml
from docopt import docopt

from .tesla import Tesla

CONFIG_FILE_PATHS = [
    os.path.join(os.path.expanduser('~'), '.tesla.yml'),
    os.path.join(os.path.expanduser('~'), '.tesla.yaml')
]


# TESLA_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
# TESLA_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
TESLA_CLIENT_ID = os.environ.get('TESLA_CLIENT_ID')
TESLA_CLIENT_SECRET = os.environ.get('TESLA_CLIENT_SECRET')
TESLA_PASSWORD = os.environ.get('TESLA_PASSWORD')


def read_config(config_file=None):
    if not config_file:
        for config_file_path in CONFIG_FILE_PATHS:
            print(config_file_path)
            if os.path.isfile(config_file_path):
                config_file = config_file_path 
                break
        else:
            raise RuntimeError('No config file found!')

    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def main():
    args = docopt(__doc__)
    config = read_config(args.get('--config-file'))

    tesla = Tesla()
    tesla.login(
        username=config.get('username'),
        password=config.get('password', TESLA_PASSWORD),
        client_id=config.get('client_id', TESLA_CLIENT_ID),
        client_secret=config.get('client_secret', TESLA_CLIENT_SECRET)
    )
    vehicles = tesla.fetch_vehicles()
    if not vehicles:
        raise RuntimeError('Unable to get vehicle id!')
    vehicle = vehicles[0]
    try:
        action = getattr(tesla, args.get('<action>').replace('-', '_').lower())
    except AttributeError:
        print('Invalid action: {0}'.format(args.get('<action>')))
        sys.exit(1)

    resp = action(vehicle.get('id'))
    pprint(resp)

if __name__ == '__main__':
    sys.exit(main())