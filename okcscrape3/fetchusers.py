import csv
import sys
import os
import json

import pandas as pd
from bs4 import BeautifulSoup

from okcscrape3 import util


def fetchusers(webdriver_path: str,
               base_url: str,
               cookies_file: str,
               usernames_file: str,
               profiles_outfile: str,
               num_profiles: int):
    print('Run fetchusers.')
    """Fetchusers procedure:
    1.  Read in usernames from usernames csv, get a list of ones that
        haven't beem fetched yet.

        Probably read in entire csv into pandas DataFrame, then filter
        by 'profile_fetched' flag.
    2.  Check if profiles csv created, if not, create it
    3.  Prepare webdriver via util.initialize_webdriver
    5.  Add cookies and whatever else to webdriver (verbosity levels, etc)
    6.  Loop through username list, earliest first
            a.  sleep
            a.  build url
            a.  get webpage
            a.  send html to parser functions
            a.  append results to the specified csv
    7.  ??
    """

    try:
        usernames_df = pd.read_csv(usernames_file, dtype={'username': str})
        # Usernames that have not had their profiles fetched yet
        usernames_to_fetch = \
            usernames_df[usernames_df['profile_fetched'] == 0] \
            .loc[:, 'username'].values
    except FileNotFoundError:
        print('Could not find csv file "{}"'.format(usernames_file))
        sys.exit()

    browser = util.initialize_webdriver(webdriver_path=webdriver_path,
                                        cookies_file=cookies_file)

    with open('profile_html_targets.json', 'r') as f:
        html_targets = json.load(f)

    for username in usernames_to_fetch[:num_profiles]:
        # Probably need try block, but what are the exceptions to catch?
        profile_dict = {}
        browser.get(base_url + 'profile/' + username)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for target in html_targets:
            name = target['name']
            attrs = target['attrs']
            target_soup = soup.find(name=name, attrs=attrs)
            profile_dict[target['label']] = target_soup.text.lower()
