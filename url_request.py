import requests

def url_request(url):
    try:
        r = requests.get(url)
    except MissingSchema:
        return (None,"NG")
    r.encoding=r.apparent_encoding
    return (r,"OK")
