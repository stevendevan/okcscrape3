#! python3
"""
@author: Steven Devan
"""

import os
import argparse
import configparser

from . import functions

"""Improvement ideas:
1.  Separate each primary function into its own file, along with a
    'global functions' file or something similar.
"""


def main():

    # Parse config.ini
    configs = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
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
                             help='Name of outfile.')
    parser_find.add_argument('--num-usernames',
                             type=int,
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

    parser_print = subparsers.add_parser('print-config',
                                         help='Print contents of config file.')

    # vars() because we need to be able to access the contents like obj[str]
    args_obj = vars(parser.parse_args())

    #

    if args_obj['save_configs']:
        for section in configs.sections():
            for key in configs[section].keys():
                if key in args_obj.keys():
                    configs.set(section, key, str(args_obj[key]))

        with open(config_path, 'w') as f:
            configs.write(f)

    if args_obj['subroutine'] == 'findusers':
        functions.findusers(args_obj)
    elif args_obj['subroutine'] == 'fetchusers':
        functions.fetchusers(args_obj)
    elif args_obj['subroutine'] == 'print-config':
        functions.print_config(configs)


if __name__ == '__main__':
    main()
