from loguru import logger as log

from pathlib import Path
import typing as t
import json

import settings
import setup
import http_lib
from core_utils import path_utils
from domain import uastring_domain

import bs4

import ua_scraper
import ua_scraper.client
import ua_scraper.constants

html_cache_dir = Path("sandbox/scrape/html_cache")
json_cache_dir = Path("sandbox/scrape/json_cache")

for d in [html_cache_dir, json_cache_dir]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)


def main():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    ua_category_link_dicts = ua_scraper.crawl_ua_categories(save_json=True)
    ua_category_links: list[uastring_domain.UACategoryIn] = []
    
    for category_link_dict in ua_category_link_dicts:
        category_links: uastring_domain.UACategoryIn = uastring_domain.UACategoryIn.model_validate(category_link_dict)
        ua_category_links.append(category_links)
        
    log.info(f"Retrieved [{len(category_links)}] category link(s)")
    log.debug(f"First 5 category links: {category_links[:5]}")

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main()