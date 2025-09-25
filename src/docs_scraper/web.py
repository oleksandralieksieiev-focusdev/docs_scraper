import requests
from config import USER_AGENT, REQUEST_TIMEOUT

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})


def fetch(url):
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")
        return None
