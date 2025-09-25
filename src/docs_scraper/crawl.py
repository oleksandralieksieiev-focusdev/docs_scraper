from collections import deque
import urllib.parse as up
import time

from utils.robots import parse_robots_txt, is_disallowed_by_robots
from utils.urls import normalize_url
from utils.paths import make_parent, url_to_path

from links.extract_links import extract_links
from links.rewrite_links import rewrite_links

from bs4 import BeautifulSoup

from web import fetch

from config import CRAWL_DELAY, BASE_URL, MAX_PAGES, OUT_DIR

class Crawler():
    def __init__(self):
        pass

    def prepare_crawl(self):
        self.robots = parse_robots_txt()
        if "crawl-delay" in self.robots:
            try:
                global CRAWL_DELAY
                CRAWL_DELAY = max(CRAWL_DELAY, float(self.robots["crawl-delay"]))
            except Exception:
                pass

        self.start = normalize_url(BASE_URL)
        self.queue = deque([self.start])
        self.visited = set()

    def crawl(self, progress):
        while self.queue:
            url = self.queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            # apply self.robots disallow check
            u_parsed = up.urlparse(url)
            if is_disallowed_by_robots(u_parsed.path, self.robots):
                print(f"[INFO] Skipping disallowed URL by self.robots.txt: {url}")
                continue

            # limit pages if requested
            if MAX_PAGES is not None and len(self.visited) > MAX_PAGES:
                break

            resp = fetch(url)
            if not resp:
                continue

            content_type = resp.headers.get("content-type", "")
            if "text/html" not in content_type:
                # not HTML — skip
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # extract links to enself.queue before rewriting

            links = extract_links(soup, url)

            # rewrite internal links and download assets
            try:
                rewrite_links(soup, url)
            except Exception as e:
                print(f"[WARN] rewrite_links failed for {url}: {e}")

            # save HTML
            out_path = url_to_path(url)
            make_parent(out_path)
            html_bytes = soup.prettify(formatter="html").encode("utf-8")
            try:
                with open(out_path, "wb") as f:
                    f.write(html_bytes)
            except Exception as e:
                print(f"[WARN] Failed to write {out_path}: {e}")
                continue

            progress.update(1)
            progress.set_postfix({"last": url})

            # enself.queue discovered links
            for link in links:
                if link not in self.visited:
                    self.queue.append(link)

            # polite delay
            time.sleep(CRAWL_DELAY)
