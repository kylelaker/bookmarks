from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

def get_page_title(url, max_len=None):
    result = requests.get(url)
    content = result.content

    soup = BeautifulSoup(content, "html.parser")
    if soup.title is None:
        return None

    if max_len is not None:
        return soup.title.text[:max_len]

    return soup.title.text

def get_favicon_link(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    icon_link = soup.find("link", rel="icon")

    if icon_link:
        return icon_link['href']

    parse = urlparse(url)
    test_link = parse.scheme + "://" + parse.netloc + "/favicon.ico"

    # If sites don't allow/block automated traffic, use the guessed favicon
    if requests.get(url).status_code in (200, 429):
        return test_link

    return None
