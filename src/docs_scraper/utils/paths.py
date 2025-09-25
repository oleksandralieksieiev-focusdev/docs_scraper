import os
import re
import urllib.parse as up
from pathlib import Path

from config import OUT_DIR

OUT_DIR.mkdir(parents=True, exist_ok=True)


def make_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def url_to_path(url):
    """Map a URL to a relative filesystem path under OUT_DIR."""
    parsed = up.urlparse(url)
    path = parsed.path
    if path.endswith("/") or path == "":
        path = path + "index.html"
    # ensure .html at the end for routes without extension
    if not os.path.splitext(path)[1]:
        path = path + ".html"
    # include query by encoding it into filename if present
    if parsed.query:
        safe_q = re.sub(r"[^0-9A-Za-z\-_.]", "_", parsed.query)
        path = path + "?" + safe_q
        # replace ? with -- for filename safety
        path = path.replace("?", "--")
    # remove leading slash
    if path.startswith("/"):
        path = path[1:]
    return OUT_DIR.joinpath(path)
