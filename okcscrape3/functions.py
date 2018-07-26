import configparser
import regex
import os

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver


def findusers(args_obj: dict) -> None:
    print('Run find.')
    homedir = os.path.dirname(__file__)
    webdriver_path = os.path.join(homedir, args_obj['webdriver_path'])
    browser = webdriver.Chrome(executable_path=webdriver_path)

    url = args_obj['base_url'] + \
        args_obj['match_url_suffix']

    html = get_webpage(browser, url, args_obj)
    usernames_list = extract_usernames_from_html(html)
    import ipdb; ipdb.set_trace()  # breakpoint b83abd5a //



def fetchusers(args_obj):
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


def get_webpage(browser, url, args_obj):
    """TODO
    """
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


def extract_usernames_from_html(html: str) -> list:
    """TODO
    """
    soup = BeautifulSoup(html, 'html.parser')
    match_cards = soup.find_all(name='div',
                                attrs={'class': 'match_card_wrapper ' +
                                       'user-not-hidden matchcard-user'})
    usernames = []
    for match_card in match_cards:
        usernames.append(match_card['data-userid'])

    return usernames
