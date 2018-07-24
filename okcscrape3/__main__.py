#! python3
"""
@author: Steven Devan
"""

import os
import csv
import argparse
import configparser

from bs4 import BeautifulSoup
from selenium import webdriver

from . import functions


def main():

    # Parse config.ini
    dirname = os.path.dirname(__file__)
    configs = configparser.ConfigParser()
    configs.read(os.path.join(dirname, 'config.ini'))

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subroutine')
    parser.add_argument('--webdriver-path',
                        default=configs['global']['webdriver_path'],
                        help='Specify the path of the webdriver.')
    parser.add_argument('--base-url',
                        default=configs['global']['base_url'], help='TODO')
    parser.add_argument('--time-between-queries', type=int,
                        default=configs['global']['time_between_queries'],
                        help='TODO')
    parser.add_argument('--max-query-attempts', type=int,
                        default=configs['global']['max_query_attempts'],
                        help='TODO')
    parser.add_argument('--no-save-configs', action='store_false',
                        default=True, dest='save_configs', help='TODO')

    parser_find = subparsers.add_parser('findusers', help='Run find.')
    parser_find.add_argument('--match-url-suffix',
                             default=configs['findusers']['match_url_suffix'],
                             help='TODO')
    parser_find.add_argument('--outfile',
                             default=configs['findusers']['usernames_outfile'],
                             help='Name of outfile.')
    parser_find.add_argument('--num-usernames',
                             default=configs['findusers']['num_usernames'],
                             help='TODO')

    parser_fetch = subparsers.add_parser('fetchusers', help='Run fetch.')
    parser_fetch.add_argument('--cookie-file', help='File containing cookies.')
    parser_fetch.add_argument('--outfile',
                              default=configs['fetchusers']['profiles_outfile'],
                              help='TODO')
    parser_fetch.add_argument('--num-profiles',
                              default=configs['fetchusers']['num_profiles'],
                              help='TODO')

    # vars() because we need to be able to access the contents like obj[str]
    args_obj = vars(parser.parse_args())

    #

    if args_obj['subroutine'] == 'findusers':
        functions.findusers(args_obj)
    elif args_obj['subroutine'] == 'fetchusers':
        functions.fetchusers(args_obj)

    if args_obj['save_configs']:
        for section in configs.sections():
            for key, value in configs[section].items():
                configs.set(section, key, value)

        with open('config.ini', 'w') as f:
            configs.write(f)


if __name__ == '__main__':
    main()
