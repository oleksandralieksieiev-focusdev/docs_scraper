from pathlib import Path

BASE_URL = "https://react.dev"
OUT_DIR = Path("output_html")  # output root
USER_AGENT = "docs_scraper v0.1 (please don't IP ban)"
MAX_PAGES = 1000  # set to an int to limit pages; None = unlimited
CRAWL_DELAY = 0.5  # seconds between requests (will respect robots.txt if present)
DOWNLOAD_ASSETS = True  # download CSS/JS/images/fonts from same origin
ASSET_SUBDIR = "assets"
REQUEST_TIMEOUT = 20
