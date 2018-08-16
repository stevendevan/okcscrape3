#!  python3
"""
@author: Steven Devan
"""

import os
import argparse
import configparser
import urllib
import zipfile

from okcscrape3.fetchusers import fetchusers
from okcscrape3.findusers import findusers
from okcscrape3.print_config import print_config
from okcscrape3.download_webdriver import download_webdriver

"""Improvement ideas:
1.  Separate each primary function into its own file, along with a
    'global functions' file or something similar.
"""


def main():
        
    # Parse config.ini
    configs = configparser.ConfigParser()
    pkg_root_path = os.path.dirname(__file__)
    config_path = os.path.join(pkg_root_path, 'config.ini')
    configs.read(config_path)

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
                             dest='usernames_outfile',
                             help='Name of outfile.')
    parser_find.add_argument('--num-usernames',
                             type=int,
                             default=configs['findusers']['num_usernames'],
                             help='TODO')

    parser_fetch = subparsers.add_parser('fetchusers', help='Run fetch.')
    parser_fetch.add_argument('--cookies-file',
                              default=configs['fetchusers']['cookies_file'],
                              help='File containing cookies.')
    parser_fetch.add_argument('--usernames-file',
                              default=configs['fetchusers']['usernames_file'],
                              help=('File of usernames of profiles to be '
                                    'fetched.'))
    parser_fetch.add_argument('--outfile',
                              default=configs['fetchusers']['profiles_outfile'],
                              dest='profiles_outfile',
                              help='TODO')
    parser_fetch.add_argument('--num-profiles',
                              default=configs['fetchusers']['num_profiles'],
                              help='TODO')

    parser_print = subparsers.add_parser('print-config',
                                         help='Print contents of config file.')

    parser_webdriver = subparsers.add_parser('download-webdriver',
                                             help='TODO')

    # vars() because we need to be able to access the contents like obj[str]
    args_obj = vars(parser.parse_args())

    # Global params
    #webdriver_path = os.path.join(pkg_root_path, args_obj['webdriver_path'])
    webdriver_path = args_obj['webdriver_path']
    base_url = args_obj['base_url']
    time_between_queries = args_obj['time_between_queries']
    max_query_attempts = args_obj['max_query_attempts']
    save_configs = args_obj['save_configs']

    if save_configs:
        _save_configs(configs, config_path, args_obj)

    if not os.path.isfile(os.path.join(pkg_root_path, webdriver_path)):
        print('The webdriver could not be found at "{}"'
              .format(webdriver_path))

    data_path = os.path.join(pkg_root_path, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # # Main subroutine branching logic # #
    if args_obj['subroutine'] == 'findusers':

        match_url_suffix = args_obj['match_url_suffix']
        usernames_outfile = args_obj['usernames_outfile']
        num_usernames = args_obj['num_usernames']

        findusers(pkg_root_path=pkg_root_path,
                  webdriver_path=webdriver_path,
                  base_url=base_url,
                  match_url_suffix=match_url_suffix,
                  usernames_outfile=usernames_outfile,
                  num_usernames=num_usernames,
                  time_between_queries=time_between_queries,
                  max_query_attempts=max_query_attempts,)
    elif args_obj['subroutine'] == 'fetchusers':

        cookies_file = args_obj['cookies_file']
        usernames_file = args_obj['usernames_file']
        profiles_outfile = args_obj['profiles_outfile']
        num_profiles = args_obj['num_profiles']

        fetchusers(pkg_root_path=pkg_root_path,
                   webdriver_path=webdriver_path,
                   usernames_file=usernames_file,
                   profiles_outfile=profiles_outfile)

    elif args_obj['subroutine'] == 'print-config':
        print_config(configs)
    elif args_obj['subroutine'] == 'download-webdriver':
        download_webdriver(pkg_root_path)


def _save_configs(configs: configparser.ConfigParser,
                  config_path: str,
                  args_obj: dict) -> None:
    """Save the current configs in the .ini file.
    """
    for section in configs.sections():
        for key in configs[section].keys():
            if key in args_obj.keys():
                configs.set(section, key, str(args_obj[key]))

    with open(config_path, 'w') as f:
        configs.write(f)

def _download_chromedriver(root_path):
    zip_file_name = "chromedriver.zip"

    urllib.request.urlretrieve("https://chromedriver.storage.googleapis.com"
                               "/2.41/chromedriver_win32.zip",
                               root_path + '\\' + zip_file_name)    
    chromeDriverZip = zipfile.ZipFile(root_path + '\\' + zip_file_name, 'r')
    chromeDriverZip.extractall(root_path)
    chromeDriverZip.close()
    os.remove(root_path + '\\' + zip_file_name)

if __name__ == '__main__':
    main()
