import configparser
import csv
import datetime
import regex
import time
import os  # pathlib also an option to consider

from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium import webdriver


def findusers(args_obj: dict) -> None:
    """Find usernames from OKCupid and log them in a csv.
    """

    """Improvement ideas:
    1.  Might need a try block for webdriver object creation.
        Once encountered a WebDriverException, which caused a freeze.
    2.  Perform rest of page parsing asynchronously with sleep timer.
        For very large username csv's, the page parsing could approach that of
        the sleep timer.
    3.  Have the csv header labels read from somewhere, as opposed to being
        hard-coded.
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
            # [3]
            writer_obj.writerow(['username', 'profile_fetched', 'date_logged'])

        usernames_list = []

    browser = webdriver.Chrome(executable_path=webdriver_path)  # [1]
    url = args_obj['base_url'] + args_obj['match_url_suffix']

    num_found_users = 0
    while num_found_users < args_obj['num_usernames']:

        # Sleep required to avoid blacklisting/throttling by OKCupid servers.
        time.sleep(args_obj['time_between_queries'])

        # [2] (applies to rest of while-loop)
        html = get_webpage(browser, url, args_obj)
        usernames_new = extract_usernames_from_html(html)

        # For csv entry. Best to have this inside the while loop in case the
        # day changes while the program is running.
        current_day = datetime.datetime.now().strftime(r'%Y%m%d')

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
    """TODO (docstring)
    """
    print('Run fetch.')


def print_config(configs: configparser.ConfigParser) -> None:
    """Print all parameters in the config.ini file in a readable format.
    """
    for section in configs.sections():
        print('[{}]'.format(section))
        for key in configs[section]:
            print('{} = {}'.format(key, configs[section][key]))
        print('')


# Internal functions below?


def get_webpage(browser: selenium.webdriver.Chrome,
                url: str,
                args_obj: dict) -> str:
    """Use selenium webdriver to fetch a webpage and return the html.
    """

    """Improvement ideas:
    1.  Look into returning page after a set amount of time.
        Some unnecessary elements take a long time to fully load.
        Would likely require args in browser obj creation or in get() function.
    """

    max_attempts = args_obj['max_query_attempts']
    for attempt in range(max_attempts):
        try:
            browser.get(url)  # [1]
        except selenium.common.exceptions.TimeoutException as e:
            if attempt < max_attempts:
                continue
            else:
                raise
        else:
            break

    return browser.page_source


def extract_usernames_from_html(html: str) -> list:
    """Pull a list of usernames from html.
    Notes:
    1.  The OKC html structure may change periodically, which will require
        this function to be updated.
    """
    soup = BeautifulSoup(html, 'html.parser')
    match_cards = soup.find_all(name='div',
                                attrs={'class': 'match_card_wrapper ' +
                                       'user-not-hidden matchcard-user'})
    usernames = []
    for match_card in match_cards:
        usernames.append(match_card['data-userid'])

    return usernames
