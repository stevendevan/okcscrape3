import configparser
import datetime
import regex
import time
import os  # pathlib also an option to consider

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver


def findusers(args_obj: dict) -> None:
    """TODO
    """
    print('Run find.')
    homedir = os.path.dirname(__file__)
    webdriver_path = os.path.join(homedir, args_obj['webdriver_path'])
    browser = webdriver.Chrome(executable_path=webdriver_path)

    url = args_obj['base_url'] + args_obj['match_url_suffix']

    html = get_webpage(browser, url, args_obj)
    usernames_list = []
    while len(usernames_list) < int(args_obj['num_usernames']):
        usernames_list += extract_usernames_from_html(html)
        print('{}/{} usernames found'
              .format(len(usernames_list), args_obj['num_usernames']))

    usernames_path = os.path.join(homedir, args_obj['outfile'])
    try:
        usernames_df = pd.read_csv(usernames_path)
    except FileNotFoundError:
        print('file "{}" does not exist, but it soon shall.'
              .format(args_obj['outfile']))
        usernames_df = pd.DataFrame()

    usernames_df_new = pd.DataFrame(
        {'profile': usernames_list,
         'profile_fetched': np.zeros(len(usernames_list), dtype=int),
         'date_found': [datetime.datetime.now().strftime(r'%Y/%m/%d')] *
         len(usernames_list)})

    usernames_df = pd.concat([usernames_df, usernames_df_new], axis=0)
    usernames_df.drop_duplicates(subset='profile', keep='first', inplace=True)
    usernames_df.to_csv(path_or_buf=usernames_path, index=False)


def fetchusers(args_obj):
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


# Internal functions?


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
