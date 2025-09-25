from config import BASE_URL, REQUEST_TIMEOUT
import urllib.parse as up

from web import session

def parse_robots_txt():
    robots_url = up.urljoin(BASE_URL, "/robots.txt")
    try:
        r = session.get(robots_url, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            return {}
        txt = r.text
        crawl = {}
        user_agent = None
        for line in txt.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("user-agent:"):
                user_agent = line.split(":", 1)[1].strip()
            elif line.lower().startswith("disallow:") and user_agent is not None:
                path = line.split(":", 1)[1].strip()
                crawl.setdefault("disallow", []).append(path)
            elif line.lower().startswith("crawl-delay:") and user_agent is not None:
                try:
                    crawl["crawl-delay"] = float(line.split(":", 1)[1].strip())
                except Exception:
                    pass
        return crawl
    except Exception:
        return {}

def is_disallowed_by_robots(path, robots):
    # naive: check if any disallow path is a prefix of the path
    dis = robots.get("disallow", [])
    for d in dis:
        if d == "":
            continue
        if path.startswith(d):
            return True
    return False
