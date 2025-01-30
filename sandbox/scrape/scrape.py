from loguru import logger as log

from pathlib import Path
import typing as t
import json

import settings
import setup
import http_lib
from core_utils import path_utils

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
    
    results: list[dict[str, list[str], str]] = []

    for ua_dict in ua_urls:
        ua_category = ua_dict["category"]
        ua_page_url = ua_dict["url"]
        
        soup = ua_scraper.get_soup(url=ua_page_url)
        log.info(f"Soup created successfully: {soup is not None}")
        soups.append(soup)
        
        output_file = path_utils.sanitize_filename(filename=f"{ua_page_url}.html")
        ua_scraper.save_soup_to_html(soup=soup, output_file=f".data/output/html_scrapes/{output_file}")
        
        ua_strings: list[str] = ua_scraper.extract_ua_strings(soup=soup)
        all_user_agents = all_user_agents + ua_strings
        
        result = {"category": ua_category, "url": ua_page_url, "user_agents": ua_strings}
        results.append(result)
        
    log.info(f"Found [{len(all_user_agents)}] user agent(s)")
    log.debug(f"Created [{len(results)}] result object(s)")


if __name__ == "__main__":
    ua_urls: list[dict[str, str]] = [
        {"category": "desktop", "url": "https://www.useragentstring.com/pages/Browserlist/"},
        {"category": "mobile", "url": "https://www.useragentstring.com/pages/Mobile%20Browserlist/"},
        {"category": "console", "url": "https://www.useragentstring.com/pages/Consolelist/"}
    ]
    
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main(ua_urls=ua_urls)