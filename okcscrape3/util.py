import json

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup

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


def extract_data_from_html(html, json_file):
    
    with open('D:\_proj\okcscrape3\sandbox\profile_html_targets.json', 'r') as f:
        instructions = json.load(f)

    soup = BeautifulSoup(html, 'html.parser')

    #data = {}
    for instruction_set in instructions:

        steps = create_linked_list(instruction_set)

        data = execute_step(soup, steps)
        import ipdb; ipdb.set_trace()  # breakpoint a11bf64a //
        junk = 1

    """
    soup_base = stuff
    for instruction_set in instructions_all
        soup_temp = soup_base
        for step in instructions_set
            for soup_temp_item in soup_temp
                if 'find'
                if 'find_all'
                    soup_temp = soup_temp.find_all(stuff)
    """
    pass


def execute_step(soup, step, data=None):
    # Found out the hard way that using a mutable default arg value is bad.
    if data is None:
        data = {}
    else:
        target = data

    step_info = step.get_val()
    action = step_info['action']
    label = step_info['label']
    rtype = step_info['rtype']
    name = step_info['name']
    attrs = step_info['attrs']

    if label is not None:
        data[label] = None

    if action == 'find':
        soup_new = soup.find(name=name, attrs=attrs)
        if rtype == 'text':
            target = soup_new.get_text(strip=True)

        if label is not None:
            data[label] = target
        else:
            data = target

        if step.has_next():            
            return execute_step(soup_new, step.get_next(), data)
        else:            
            return data

    elif action == 'find_all':

        soup_list = soup.find_all(name=name, attrs=attrs)
        data_new = []
        for soup_item in soup_list:
            if rtype == 'text':
                data_new.append(soup_item.text)
            elif step.has_next():
                data_new.append(execute_step(soup_item, step.get_next()))
            else:
                raise SystemExit('find_all else condition hit')


def create_linked_list(normal_list):
    head_old = Node(normal_list[-1])
    for element in normal_list[-2::-1]:
        head_new = Node(element)
        head_new.set_next(head_old)
        head_old = head_new

    return head_old


#class LinkedList(object):
#    def __init__(self, head=None):
#        self.head = head
#
#    def insert(self, data):
#        new_node = Node(data)
#        new_node.set_next(self.head)
#        self.head = new_node


class Node(object):
    def __init__(self, node_info):
        self.val = node_info
        self.next = None

    def get_val(self):
        return self.val

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next

    def has_next(self):
        return self.next is not None
