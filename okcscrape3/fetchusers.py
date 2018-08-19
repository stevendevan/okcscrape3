import csv
import sys
import os

import pandas as pd

from okcscrape3 import util


def fetchusers(webdriver_path: str,
               cookies_file: str,
               usernames_file: str,
               profiles_outfile: str):
    print('Run fetchusers.')
    """Checklist
    1.  Read in usernames from usernames csv, get a list of ones that
        haven't beem fetched yet.

        Probably read in entire csv into pandas DataFrame, then filter
        by 'profile_fetched' flag.
    2.  Check if profiles csv created, if not, create it
    3.  Load in cookies file (json?)
    4.  Create webdriver
    5.  Add cookies and whatever else to webdriver (verbosity levels, etc)
    6.  Loop through username list, earliest first
            a.  sleep
            a.  build url
            a.  get webpage
            a.  send html to parser functions
            a.  append results to the specified csv
    7.  ??
    """

    #usernames_path = os.path.join(pkg_root_path, usernames_file)
    #profiles_path = os.path.join(pkg_root_path, profiles_outfile)
    #webdriver_path = os.path.join(pkg_root_path, webdriver_path)

    try:
        usernames_df = pd.read_csv(usernames_file)
        # Usernames that have not had their profiles fetched yet
        usernames_to_fetch = \
            usernames_df[usernames_df['profile_fetched'] == 0] \
            .loc[:, 'username']
    except FileNotFoundError:
        print('Could not find csv file "{}"'.format(usernames_file))
        sys.exit()
