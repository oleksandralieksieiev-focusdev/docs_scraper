import urllib.parse as up
from config import BASE_URL

def same_origin(url):
    p = up.urlparse(url)
    base = up.urlparse(BASE_URL)
    return (p.scheme in ("http", "https")) and (p.netloc == base.netloc)

def normalize_url(url, base=BASE_URL):
    return up.urljoin(base, url.split("#")[0].strip())
