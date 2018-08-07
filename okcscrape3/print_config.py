import configparser

#

#


def print_config(configs: configparser.ConfigParser) -> None:
    """Print all parameters in the config.ini file in a readable format.
    """
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')
