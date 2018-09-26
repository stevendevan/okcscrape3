import pickle as pkl
import os
import json

from selenium import webdriver
from bs4 import BeautifulSoup

from okcscrape3 import util

def prepare_webdriver():
    webdriver_path = os.path.join(os.path.dirname(__file__),
                                  'chromedriver.exe')
    browser = webdriver.Chrome(webdriver_path, service_args=['--silent'])
    with open('cookies.pickle', 'rb') as f:
        cookies = pkl.load(f)

    browser.get('https://www.okcupid.com')

    for cookie in cookies:
        browser.add_cookie(cookie)

    return browser


def scrape_options(browser: webdriver.Chrome):
    with open('D:\_proj\okcscrape3\sandbox\profile_options_source.json', 'r') as f:
        instructions = json.load(f)

    profile_options = {}
    temp_html = ''
    temp_soup = None
    for step in instructions:
        action = step['action']
        if action == 'button':
            button_selector = step['selector']
            button = browser.find_element_by_css_selector(button_selector)
            button.click()
        elif action == 'find':
            name = step['name']
            attrs = step['attrs']
            temp_html = browser.page_source
            temp_soup = BeautifulSoup(temp_html, 'html.parser')
            temp_soup = temp_soup.find(name=name, attrs=attrs)
        elif action == 'find_all':
            name = step['name']
            attrs = step['attrs']
            options_list = []
            if not temp_html:
                temp_html = browser.page_source
                temp_soup = BeautifulSoup(temp_html, 'html.parser')
            temp_soup = temp_soup.find_all(name=name, attrs=attrs)
            for soup_option in temp_soup:
                keyword = soup_option.text
                # Skip if the keyword consists of all punctuation, e.g. '-'
                if any(map(lambda char: char.isalnum(), keyword)):
                    options_list.append(keyword.lower())
            temp_html = ''
            temp_soup = None

            profile_options[step['label']] = options_list


def nav_to_profile(browser, profile: str):
    browser.get('https://www.okcupid.com/profile/' + profile)


def nav_to_me(browser):
    browser.get('https://www.okcupid.com/profile')


def main():
    
    base_path = os.path.dirname(__file__)
    okcscrape3_path = 'D:\_proj\okcscrape3\okcscrape3'
    usernames_targets_file = os.path.join(okcscrape3_path, 'usernames_html_targets.json')
    profile_targets_file = os.path.join(okcscrape3_path, 'profile_html_targets.json')
    profile_options_file = os.path.join(okcscrape3_path, 'options_html_targets.json')

    profile_html_path = os.path.join(base_path, 'sample_profile_html.txt')
    match_html_path = os.path.join(base_path, 'sample_match_html.txt')

    with open(profile_html_path, 'r', encoding='utf-8') as f:
        profile_html = f.read()

    with open(match_html_path, 'r', encoding='utf-8') as f:
        match_html = f.read()

    browser = prepare_webdriver()
    nav_to_me(browser)
    options_html = browser.page_source
    """
    profile_data = util.extract_data_from_html(browser,
                                               profile_html,
                                               profile_targets_file)
    usernames_data = util.extract_data_from_html(browser,
                                                 match_html,
                                                 usernames_targets_file)
    """
    profile_options = util.extract_data_from_html(browser,
                                                  options_html,
                                                  profile_options_file)

    import ipdb; ipdb.set_trace()  # breakpoint 6a9b8eb5 //


if __name__ == '__main__':
    main()