import os
import urllib.parse as up

from utils.urls import normalize_url, same_origin
from utils.paths import url_to_path
from fs import save_asset

from config import OUT_DIR, DOWNLOAD_ASSETS

def rewrite_links(soup, page_url):
    # rewrite <a href>, <img src>, <link href>, <script src>, <source src> etc.
    # For same-origin HTML pages, rewrite to local relative paths.
    # For assets, optionally download and rewrite to local assets/.
    tags_attrs = [
        ("a", "href"),
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("source", "src"),
        ("iframe", "src"),
    ]
    for tag_name, attr in tags_attrs:
        for tag in soup.find_all(tag_name):
            if not tag.has_attr(attr):
                continue
            orig = tag[attr]
            if orig.startswith("mailto:") or orig.startswith("tel:") or orig.startswith("javascript:"):
                continue
            full = normalize_url(orig, base=page_url)
            if not full.startswith("http"):
                continue
            # only handle same-origin links for rewriting
            if same_origin(full):
                # if it's an HTML page (no asset extension), rewrite to local file path
                p_ext = os.path.splitext(up.urlparse(full).path)[1].lower()
                if p_ext in ("", ".html", ".htm") or full.rstrip("/").endswith("/"):
                    # map to saved file
                    dest_path = url_to_path(full)
                    rel = os.path.relpath(dest_path, start=url_to_path(page_url).parent)
                    rel = rel.replace(os.path.sep, "/")
                    tag[attr] = rel
                else:
                    # it's an asset (css/js/img/font). Optionally download
                    if DOWNLOAD_ASSETS:
                        local_rel = save_asset(full, referer=page_url)
                        if local_rel:
                            rel = os.path.relpath(OUT_DIR.joinpath(local_rel), start=url_to_path(page_url).parent)
                            tag[attr] = rel.replace(os.path.sep, "/")
                        else:
                            tag[attr] = full
                    else:
                        tag[attr] = full
            else:
                # external link: leave absolute
                tag[attr] = full
