import os
import urllib.parse as up

from utils.urls import normalize_url

from config import BASE_URL


def extract_links(soup, page_url):
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        full = normalize_url(href, base=page_url)
        if full.startswith(BASE_URL):
            # only add same-origin pages (avoid assets and anchors)
            parsed = up.urlparse(full)
            # ignore fragments
            full = up.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', parsed.query, ''))
            # filter out obvious binary assets by extension
            ext = os.path.splitext(parsed.path)[1].lower()
            if ext in (".pdf", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".webm"):
                continue
            links.add(full)
    return links
