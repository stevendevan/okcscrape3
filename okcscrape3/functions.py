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
    usernames_path = os.path.join(homedir, args_obj['outfile'])
    webdriver_path = os.path.join(homedir, args_obj['webdriver_path'])

    # Get dict from csv
    # Get list of profiles from dict
    try:
        usernames_df = pd.read_csv(usernames_path)
    except FileNotFoundError:
        print('file "{}" does not exist, but it soon shall.'
              .format(args_obj['outfile']))
        usernames_df = pd.DataFrame()

    browser = webdriver.Chrome(executable_path=webdriver_path)
    url = args_obj['base_url'] + args_obj['match_url_suffix']

    usernames_list = []
    num_existing_users = len(usernames_df['profile'].values)
    num_found_users = 0
    # While counter of new profiles < num_usernames
    while num_found_users < args_obj['num_usernames']:
        time.sleep(args_obj['time_between_queries'])
        html = get_webpage(browser, url, args_obj)
        usernames_list += extract_usernames_from_html(html)

        # for username in new usernames
        #   check if it's in the list of profiles
        #   if not:
        #       write to csv
        #       add to list of profiles
        #       increment counter of new unique profiles
        #       if counter == num_usernames
        #           break

        # Maybe turn this into a private function for clarity
        num_found_users = len(set(list(usernames_df['profile'].values) +
                                  usernames_list)) - \
            num_existing_users

        print('{}/{} usernames found'
              .format(num_found_users, args_obj['num_usernames']))

    usernames_df_new = pd.DataFrame(
        {'profile': usernames_list[0:args_obj['num_usernames']],
         'profile_fetched': np.zeros(args_obj['num_usernames'], dtype=int),
         'date_found': [datetime.datetime.now().strftime(r'%Y/%m/%d')] *
         args_obj['num_usernames']})

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
