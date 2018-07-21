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

from . import find
import ipdb; ipdb.set_trace()  # breakpoint d4eb54b0 //


def main():

    # Parse config.ini
    configs = configparser.ConfigParser()
    configs.read('config.ini')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '--driver-path', help='Specify the path of the webdriver.')
    parser.add_argument('--base-url', type=str,
                        default=configs['global']['BASE_URL'], help='TODO')

    parser_find = subparsers.add_parser('find', help='Run find.')
    parser_find.add_argument('--outfile', help='Name of outfile.')

    parser_fetch = subparsers.add_parser('fetch', help='Run fetch.')
    parser_fetch.add_argument('--cookie-file', help='File containing cookies.')

    args = parser.parse_args()

    #

    find.find(args.base_url)


if __name__ == '__main__':
    main()
