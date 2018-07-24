import configparser

def findusers(thing):
    print('Run find.')
    print(thing)


def fetchusers(args_obj):
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


def get_webpage(browser, url):
    print('Get webpage.')
