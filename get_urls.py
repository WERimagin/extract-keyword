import MeCab
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os
from urllib.parse import urlparse,urljoin

def get_urls(url,size):
    try:
        r = requests.get(url)
    except:
        return []
    r.encoding=r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    urls=[url]
    url_parse=urlparse(url)
    for link in soup.find("body").find_all("a"):
        link_url=link.get("href")
        link_url_parse=urlparse(link_url)
        #if link_url_parse.path[-4:]=="html" and (url_parse.netloc==link_url_parse.netloc or link_url_parse.netloc==""):
        if url_parse.netloc==link_url_parse.netloc or link_url_parse.netloc=="":
            urls.append("http://"+url_parse.netloc+link_url_parse.path)

    return urls[0:size]
