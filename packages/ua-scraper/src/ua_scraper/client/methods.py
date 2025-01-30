from loguru import logger as log

import typing as t
import json

import http_lib

import bs4
import httpx


def get_soup(url: str, headers: dict | None = None, parser: str = "html.parser") -> bs4.BeautifulSoup | None:
    req = http_lib.build_request(url=url, headers=headers)
    
    log.info(f"Scraping URL: {url}")
    try:
        with http_lib.get_http_controller() as http_ctl:
            res = http_ctl.send_request(req)
            res.raise_for_status()
    except Exception as exc:
        msg = f"({type(exc)}) Error scraping URL '{url}'. Details: {exc}"
        log.error(msg)
        
        raise exc
    
    if not res.status_code == 200:
        log.warning(f"Non-200 response code: [{res.status_code}: {res.reason_phrase}]: {res.text}")
        return
        
    log.info(f"Response: [{res.status_code}: {res.reason_phrase}]")
    
    try:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(res.text, parser)
        log.success(f"Scraped '{url}' & converted to BeautifulSoup object.")
        return soup
    except Exception as exc:
        msg= f"({type(exc)}) Error converting scrape to BeautifulSoup. Details: {exc}"
        log.error(msg)
        
        raise exc

