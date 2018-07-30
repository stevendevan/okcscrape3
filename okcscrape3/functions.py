import configparser
import csv
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

    try:
        usernames_df = pd.read_csv(usernames_path, dtype={'username': str})
        usernames_list = usernames_df['username'].values
    except FileNotFoundError:
        print('file "{}" does not exist, but it soon shall.'
              .format(args_obj['outfile']))
        with open(usernames_path, 'w') as f:
            writer_obj = csv.writer(f, lineterminator='\n')
            writer_obj.writerow(['username', 'profile_fetched', 'date_logged'])

        usernames_list = []

    # Once encountered a WebDriverException here, caused freeze
    browser = webdriver.Chrome(executable_path=webdriver_path)
    url = args_obj['base_url'] + args_obj['match_url_suffix']

    num_found_users = 0
    while num_found_users < args_obj['num_usernames']:

        current_day = datetime.datetime.now().strftime(r'%Y%m%d')
        # Maybe async sleep with the rest of the loop operations?
        time.sleep(args_obj['time_between_queries'])
        html = get_webpage(browser, url, args_obj)
        usernames_new = extract_usernames_from_html(html)

        for username in usernames_new:
            if username not in usernames_list:
                data_to_write = [username, 0, current_day]

                with open(usernames_path, 'a') as f:
                    writer_obj = csv.writer(f, lineterminator='\n')
                    writer_obj.writerow(data_to_write)

                usernames_list += username
                num_found_users += 1

                if num_found_users == args_obj['num_usernames']:
                    break

        print('{}/{} usernames found'
              .format(num_found_users, args_obj['num_usernames']))


def fetchusers(args_obj):
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


# Internal functions?


def get_webpage(browser: selenium.webdriver.Chrome,
                url: str,
                args_obj: dict) -> str:
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
