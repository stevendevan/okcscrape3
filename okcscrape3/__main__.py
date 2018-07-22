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
    configs = configparser.ConfigParser()
    configs.read('config.ini')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser.add_argument('--webdriver-path', type=str,
                        default=configs['global']['webdriver_path'],
                        help='Specify the path of the webdriver.')
    parser.add_argument('--base-url', type=str,
                        default=configs['global']['base_url'], help='TODO')
    parser.add_argument('--time-between-queries', type=int,
                        default=configs['global']['time_between_queries'],
                        help='TODO')
    parser.add_argument('--save-configs', type=bool,
                        action='store_true', help='TODO')

    parser_find = subparsers.add_parser('find', help='Run find.')
    parser_find.add_argument('--outfile', help='Name of outfile.')

    parser_fetch = subparsers.add_parser('fetch', help='Run fetch.')
    parser_fetch.add_argument('--cookie-file', help='File containing cookies.')

    args_obj = parser.parse_args()

    #

    if args_obj.find:
        functions.find(args_obj)
    elif args_obj.fetch:
        functions.fetch(args_obj)

    if args_obj.save_configs:
        for section in configs.sections():
            for key, value in configs[section].items():
                configs.set(section, key, value)

        with open('config.ini', 'w') as f:
            configs.write(f)


if __name__ == '__main__':
    main()
