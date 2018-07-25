import configparser
import os

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver


def findusers(args_obj: dict) -> None:
    print('Run find.')
    webdriver_path = os.path.join(os.path.dirname(__file__),
                                  args_obj['webdriver_path'])
    browser = webdriver.Chrome(executable_path=webdriver_path)

    url = args_obj['base_url'] + \
        args_obj['match_url_suffix']

    html = get_webpage(browser, url, args_obj)


def fetchusers(args_obj):
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


def get_webpage(browser, url, args_obj):
    # Look into returning page after a set amount of time.
    # Some unnecessary elements take a long time to fully load.

    max_attempts = args_obj['max_query_attempts']
    for attempt in range(max_attempts):
        try:
            browser.get(url)
        except selenium.common.exceptions.TimeoutException as e:
            if attempt < max_attempts:
                continue
            else:
                raise
        else:
            break

    return browser.page_source
