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

