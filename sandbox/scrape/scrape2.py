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
import ua_scraper.constants

html_cache_dir = Path("sandbox/scrape/html_cache")
json_cache_dir = Path("sandbox/scrape/json_cache")

for d in [html_cache_dir, json_cache_dir]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)


def main():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    ua_strings = ua_scraper.crawl_ua_categories()

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main()