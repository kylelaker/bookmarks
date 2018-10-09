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
    icon_link = soup.find("link", rel="shortcut icon")

    if icon_link and 'href' in icon_link:
        return icon_link['href']

    parse = urlparse(url)
    return parse.scheme + "://" + parse.netloc + "/favicon.ico"
