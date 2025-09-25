import urllib.parse as up
from web import fetch
from pathlib import Path
import os

from utils.urls import normalize_url, same_origin
from utils.paths import make_parent

from config import OUT_DIR, ASSET_SUBDIR


def save_asset(url, referer):
    url = normalize_url(url, base=referer)
    if not same_origin(url):
        return None
    resp = fetch(url)
    if not resp:
        return None
    parsed = up.urlparse(url)
    filename = os.path.basename(parsed.path) or "asset"
    # preserve extension from path
    if not os.path.splitext(filename)[1]:
        # try guess from content-type
        ct = resp.headers.get("content-type", "")
        ext = ""
        if "javascript" in ct:
            ext = ".js"
        elif "css" in ct:
            ext = ".css"
        elif "font" in ct or "woff" in ct or "ttf" in ct:
            ext = os.path.splitext(parsed.path)[1] or ""
        filename += ext
    # make directories mirror path
    rel_path = Path(ASSET_SUBDIR) / parsed.path.lstrip("/")
    if rel_path.name == "":
        rel_path = rel_path / filename
    local_path = OUT_DIR.joinpath(rel_path)
    make_parent(local_path)
    try:
        with open(local_path, "wb") as f:
            f.write(resp.content)
        return local_path.relative_to(OUT_DIR).as_posix()
    except Exception as e:
        print(f"[WARN] Could not save asset {url}: {e}")
        return None
