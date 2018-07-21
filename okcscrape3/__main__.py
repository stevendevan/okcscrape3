#! python3
"""
@author: Steven Devan
"""

import csv
import argparse
import configparser

from bs4 import BeautifulSoup
from selenium import webdriver


def main():

    # Parse config.ini
    configs = configparser.ConfigParser()
    configs.read('config.ini')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '--driver-path', help='Specify the path of the webdriver.')

    parser_find = subparsers.add_parser('find', help='Run find.')
    parser_find.add_argument('--outfile', help='Name of outfile.')

    parser_fetch = subparsers.add_parser('fetch', help='Run fetch.')
    parser_fetch.add_argument('--cookie-file', help='File containing cookies.')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
