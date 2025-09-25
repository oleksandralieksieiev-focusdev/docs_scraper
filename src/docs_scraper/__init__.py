#!/usr/bin/env python3

from crawl import Crawler
from tqdm import tqdm

from config import OUT_DIR

if __name__ == "__main__":
    crawler = Crawler()
    crawler.prepare_crawl()

    progress = tqdm(total=0, unit=" pages", desc="pages")
    crawler.crawl(progress)
    progress.close()

    print(f"Done. Saved {len(list(OUT_DIR.rglob('*.html')))} HTML files under {OUT_DIR}")
