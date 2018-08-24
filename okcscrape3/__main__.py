#!  python3
"""
@author: Steven Devan
"""

import os
import argparse
import configparser

from okcscrape3.fetchusers import fetchusers
from okcscrape3.findusers import findusers
from okcscrape3.print_config import print_config
from okcscrape3.download_webdriver import download_webdriver

"""Improvement ideas (missing #s already completed):
2.  Automate arg parser generation/setup by pulling subparser and arg info
    from a .json or something similar.
3.  Externalize webdriver initialization, probably to util.py, similar to
    util.get_webpage currently.
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
                        help='Specify the path of the webdriver. Can be '
                             'relative to the package root path or absolute.')
    parser.add_argument('--base-url',
                        default=configs['global']['base_url'],
                        help='The base url for the OKCupid website.')
    parser.add_argument('--time-between-queries',
                        type=int,
                        default=configs['global']['time_between_queries'],
                        help='Time in seconds to sleep between each webpage '
                             'request. This is to avoid '
                             'throttling/blacklisting by OKC servers.')
    parser.add_argument('--max-query-attempts',
                        type=int,
                        default=configs['global']['max_query_attempts'],
                        help='The number of attempts to make when requesting '
                             'a webpage, in case the first request is not '
                             'successful.')
    parser.add_argument('--no-save-configs',
                        action='store_false',
                        default=True,
                        dest='save_configs',
                        help='If used, any other cl-args provided are not '
                             'saved to the config.ini file. This arg does '
                             'not require a value.')

    parser_find = subparsers.add_parser('findusers',
                                        help='Find random OKCupid usernames '
                                             'and log them in a csv.')
    parser_find.add_argument('--match-url-suffix',
                             default=configs['findusers']['match_url_suffix'],
                             help='i.e. base_url + match_url_suffix = "OKC '
                                  'browse users page", from which the '
                                  'usernames are collected.')
    parser_find.add_argument('--outfile',
                             default=configs['findusers']['usernames_outfile'],
                             dest='usernames_outfile',
                             help='Name or absolute path of the csv in which '
                                  'to store the collected usernames.')
    parser_find.add_argument('--num-usernames',
                             type=int,
                             default=configs['findusers']['num_usernames'],
                             help='Integer specifying the number of random '
                                  'usernames to collect.')

    parser_fetch = subparsers.add_parser('fetchusers',
                                         help='Given a list of usernames, '
                                              'navigate to each user\'s '
                                              'profile and log the contents '
                                              'in a csv.')
    parser_fetch.add_argument('--cookies-file',
                              default=configs['fetchusers']['cookies_file'],
                              help='Name or absolute path to the .json file '
                                   'containing the OKC cookies (credentials) '
                                   'necessary to view user profiles.')
    parser_fetch.add_argument('--usernames-file',
                              default=configs['fetchusers']['usernames_file'],
                              help=('Name or absolute path of a usernames csv '
                                    'from which to get a list of usernames '
                                    'of which to fetch the profiles.'))
    parser_fetch.add_argument('--outfile',
                              default=configs['fetchusers']['profiles_outfile'],
                              dest='profiles_outfile',
                              help='Name or absolute path of the csv in which '
                                   'to store user profile information.')
    parser_fetch.add_argument('--num-profiles',
                              type=int,
                              default=configs['fetchusers']['num_profiles'],
                              help='Integer specifying the number of profiles '
                                   'to fetch.')

    parser_print = subparsers.add_parser('print-config',
                                         help='Print contents of config file.')

    parser_webdriver = subparsers.add_parser('download-webdriver',
                                             help='Download the '
                                                  '"chromedriver.exe" headless'
                                                  ' web browser that selenium '
                                                  'will use to navigate OKC.')

    # vars() because we need to be able to access the contents like obj[str]
    args_obj = vars(parser.parse_args())

    # Global params
    webdriver_path = os.path.join(pkg_root_path, args_obj['webdriver_path'])
    base_url = args_obj['base_url']
    time_between_queries = args_obj['time_between_queries']
    max_query_attempts = args_obj['max_query_attempts']
    save_configs = args_obj['save_configs']

    if save_configs:
        _save_configs(configs, config_path, args_obj)

    data_path = os.path.join(pkg_root_path, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # # Main subroutine branching logic # #
    if args_obj['subroutine'] == 'findusers':

        match_url_suffix = args_obj['match_url_suffix']
        usernames_outfile = os.path.join(pkg_root_path,
                                         args_obj['usernames_outfile'])
        num_usernames = args_obj['num_usernames']

        findusers(webdriver_path=webdriver_path,
                  base_url=base_url,
                  time_between_queries=time_between_queries,
                  max_query_attempts=max_query_attempts,

                  match_url_suffix=match_url_suffix,
                  usernames_outfile=usernames_outfile,
                  num_usernames=num_usernames,)

    elif args_obj['subroutine'] == 'fetchusers':

        cookies_file = os.path.join(pkg_root_path,
                                    args_obj['cookies_file'])
        usernames_file = os.path.join(pkg_root_path,
                                      args_obj['usernames_file'])
        profiles_outfile = os.path.join(pkg_root_path,
                                        args_obj['profiles_outfile'])
        num_profiles = args_obj['num_profiles']
        profile_html_targets_file = os.path.join(pkg_root_path,
                                                 configs['profile_html_targets_file'])

        fetchusers(webdriver_path=webdriver_path,
                   base_url=base_url,
                   time_between_queries=time_between_queries,
                   max_query_attempts=max_query_attempts,

                   cookies_file=cookies_file,
                   usernames_file=usernames_file,
                   profiles_outfile=profiles_outfile,
                   num_profiles=num_profiles,

                   profile_html_targets_file=profile_html_targets_file,)

    elif args_obj['subroutine'] == 'print-config':
        print_config(configs)
    elif args_obj['subroutine'] == 'download-webdriver':
        download_webdriver(webdriver_path)
    else:
        parser.print_help()


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


if __name__ == '__main__':
    main()
