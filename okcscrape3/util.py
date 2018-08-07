import selenium


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
