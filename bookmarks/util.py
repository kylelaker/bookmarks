from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from bookmarks import app


_CACHE = {}


def get_head(url):
    """
    Get the head element of an HTML document. Store it in the cache keyed by the URL.

    :param url: The page's head to retrieve
    :return: The page's head
    """

    if url not in _CACHE:
        result = requests.get(url)
        if not result.ok:
            return None

        content = result.content
        soup = BeautifulSoup(content, "html.parser")
        _CACHE[url] = str(soup.head)

    return _CACHE[url]


def get_page_title(url, max_len=None):
    """
    Get the HTML title element for a page.

    :param url: The url to get the title for
    :param max_len: The maximum length of the title. The title will be truncated to this length. Default is None
    :return: The title for the page
    """

    head = get_head(url)
    if not head:
        return None

    soup = BeautifulSoup(head, "html.parser")

    if soup.title is None:
        return None

    if max_len is not None:
        return soup.title.text[:max_len]

    return soup.title.text


def get_favicon_link(url):
    """
    Get the favicon URL for a provided page. The page will be checked for an `icon` link element. If that does not
    exist, an attempt will be made to check the domain's /favicon.ico. If that does not exist, None is returned.

    :param url: The URL to grab the favicon for
    :return: The URL for the favicon
    """

    head = get_head(url)

    # If unable to get the <head>, just try /favicon.ico
    if not head:
        return _naive_favicon(url)

    soup = BeautifulSoup(head, "html.parser")
    icon_link = soup.find("link", rel="icon")
    is_absolute = icon_link and bool(urlparse(icon_link['href']).scheme)

    # If the page provides a link and it's not a relative URL, use it. Otherwise, guess one.
    if is_absolute:
        test_link = icon_link['href']
    elif icon_link:
        test_link = _relative_favicon_link(url, icon_link)
    else:
        return _naive_favicon(url)

    app.logger.debug("Trying %s", test_link)

    # If sites don't allow automated traffic, use the guessed favicon
    if requests.head(test_link).ok:
        return test_link

    return None


def _relative_favicon_link(url, icon_link):
    """
    Get the link for a favicon when given a relative link

    :param url: The URL the favicon is for
    :param icon_link: The icon <link> tag
    :return: The url for the favicon
    """

    parse = urlparse(url)
    if str(parse.path).endswith("/") or icon_link['href'].startswith("/"):
        path_sep = ""
    else:
        path_sep = "/"

    return parse.scheme + "://" + parse.netloc + parse.path + path_sep + icon_link['href']


def _naive_favicon(url):
    """
    Just get /favicon.ico for the domain.

    :param url: The original query
    :return: <domain>/favicon.ico
    """

    parse = urlparse(url)
    test_link = parse.scheme + "://" + parse.netloc + "/favicon.ico"
    app.logger.debug("Trying %s", test_link)
    if requests.head(test_link).ok:
        return test_link
