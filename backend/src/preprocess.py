import re
from urllib.parse import urlparse

def extract_urls(text):
    if not text: return []
    urls = re.findall(r'http[s]?://\S+|www\.\S+', text)
    return urls

def domain_of(url):
    try:
        if not url.startswith('http'):
            url = 'http://' + url
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ''
