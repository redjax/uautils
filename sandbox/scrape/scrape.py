from loguru import logger as log

from pathlib import Path
import typing as t
import json

import settings
import setup
import http_lib

import bs4

import ua_scraper
import ua_scraper.client

html_cache_dir = Path("sandbox/scrape/html_cache")

if not html_cache_dir.exists():
    html_cache_dir.mkdir(parents=True, exist_ok=True)


def main(ua_urls: list[dict[str, str]]):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    all_user_agents: list[dict[str, t.Union[str, dict[str, str]]]] = []
    soups: list[bs4.BeautifulSoup] = []

    for ua_dict in ua_urls:
        ua_category = ua_dict["category"]
        ua_page_url = ua_dict["url"]
        
        soup = ua_scraper.client.get_soup(url=ua_page_url)
        log.info(f"Soup created successfully: {soup is not None}")

if __name__ == "__main__":
    ua_urls: list[dict[str, str]] = [
        {"category": "desktop", "url": "https://www.useragentstring.com/pages/Browserlist/"},
        {"category": "mobile", "url": "https://www.useragentstring.com/pages/Mobile%20Browserlist/"},
        {"category": "console", "url": "https://www.useragentstring.com/pages/Consolelist/"}
    ]
    
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main(ua_urls=ua_urls)