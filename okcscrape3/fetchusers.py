#

import pandas as pd

from okcscrape3 import util


def fetchusers():
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
