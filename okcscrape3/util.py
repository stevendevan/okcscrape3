import json

import selenium
from selenium import webdriver

#


def initialize_webdriver(webdriver_path: str,
                         base_url='https://www.okcupid.com',
                         cookies_file=None) -> webdriver.Chrome:
    try:
        browser = webdriver.Chrome(executable_path=webdriver_path)

    except selenium.common.exceptions.WebDriverException as e:
        print('An exception has occurred while attempting to initialize '
              'the webdriver at "{}". This is most likely beccause the '
              'file doesn\'t exist at the specified location. You can also '
              'download the webdriver with the "download-webdriver" command.'
              .format(webdriver_path))
        raise SystemExit

    if cookies_file:
        try:
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)

        except FileNotFoundError as e:
            print('Could not find the cookies file at "{}"'
                  .format(cookies_file))
            browser.quit()
        else:
            # Must navigate to the correct domain before assigning cookies.
            browser.get(base_url)
            for cookie in cookies:
                browser.add_cookie(cookie)

    return browser


def get_webpage(browser: selenium.webdriver.Chrome,
                url: str,
                max_query_attempts: int) -> str:
    """Use selenium webdriver to fetch a webpage and return the html.
    """

    """Improvement ideas:
    1.  Look into returning page after a set amount of time.
        Some unnecessary elements take a long time to fully load.
        Would likely require args in browser obj creation or in get() function.
    """

    for attempt in range(max_query_attempts):
        try:
            browser.get(url)  # [1]
        except selenium.common.exceptions.TimeoutException as e:
            if attempt < max_query_attempts:
                continue
            else:
                raise
        else:
            break

    return browser.page_source
