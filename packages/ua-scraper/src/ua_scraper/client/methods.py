from loguru import logger as log

import typing as t
import json
from pathlib import Path
import time

import http_lib

import bs4
import httpx

from core_utils import path_utils

from ..constants import ALL_UA_URL, DESKOP_UA_URL, MOBILE_UA_URL, CONSOLE_UA_URL, UASTRING_BASE_URL, UASTRING_CATEGORIES, UASTRING_PAGES_URL


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


def extract_ua_strings(soup: bs4.BeautifulSoup) -> list[str]:
    user_agents: list[str] = []
    
    ## Extract the 'liste' div that has all the user agents
    list_div: bs4.Tag = soup.find("div", attrs={"id": "liste"})
    # log.debug(f"UA list div ({type(list_div)}): {list_div}")
        
    ## Extract individual <ul> lists on page
    ua_lists: bs4.ResultSet[bs4.Tag] = list_div.find_all("ul")
    # log.debug(f"UA lists ({type(ua_lists)}): {ua_lists}")
    
    ## Loop over lists of UA strings
    for ua_list in ua_lists:
        # log.info("Extracting <a> tags from soup")
        ## Grab all links
        links: bs4.ResultSet[bs4.Tag] = ua_list.find_all("a")
        
        # log.info("Creating list of UA strings from soup")
        link_texts = [link.text for link in links]
        # log.debug(f"Link type: ({type(link_texts[0])})")
        
        ## Add UA strings to list
        user_agents = user_agents + link_texts
        
    log.debug(f"Found [{len(user_agents)}] UA string(s)")
    log.debug(f"Preview 5 UA strings: {user_agents[:5]}")
    
    return user_agents


def save_soup_to_html(soup: bs4.BeautifulSoup, output_file: t.Union[str, Path]):
    output_file: Path = Path(str(output_file)).expanduser() if "~" in (str(output_file)) else Path(str(output_file))
    
    if not output_file.parent.exists():
        log.warning(f"HTML output directory '{output_file.parent}' does not exist. Creating directory.")
        
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"Permission denied creating path '{output_file.parent}'.")
        except Exception as exc:
            msg = f"({type(exc)}) Error creating HTML output directory '{output_file.parent}'. Details: {exc}"
            log.error(msg)
            
            raise exc
    
    log.info(f"Saving BeautifulSoup object to HTML file: {output_file}")
    try:
        with open(output_file, "w") as f:
            _soup = soup.prettify()
            
            f.write(_soup)
            log.success(f"BeautifulSoup saved as HTML to path: {output_file}")
            
            return True
    except Exception as exc:
        msg = f"({type(exc)}) Error saving BeautifulSoup to HTML file at path: {output_file}. Details: {exc}"
        log.error(msg)
        
        raise exc


def save_scrape_results_to_json(scrape_results: list[dict], output_file: t.Union[str, Path]):
    output_file: Path = Path(str(output_file)).expanduser() if "~" in (str(output_file)) else Path(str(output_file))
    
    if not output_file.parent.exists():
        log.warning(f"HTML output directory '{output_file.parent}' does not exist. Creating directory.")
        
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"Permission denied creating path '{output_file.parent}'.")
        except Exception as exc:
            msg = f"({type(exc)}) Error creating HTML output directory '{output_file.parent}'. Details: {exc}"
            log.error(msg)
            
            raise exc
    
    log.info(f"Saving BeautifulSoup object to HTML file: {output_file}")
    try:
        with open(output_file, "w") as f:
            _data = json.dumps(scrape_results, indent=4, sort_keys=True, default=str)
            f.write(_data)
            log.success(f"UA string scrape results saved to path: {output_file}")
            
            return True
    except Exception as exc:
        msg = f"({type(exc)}) Error saving BeautifulSoup to HTML file at path: {output_file}. Details: {exc}"
        log.error(msg)
        
        raise exc


def scrape_ua_categories(url: str = UASTRING_CATEGORIES, headers: dict | None = None, parser: str = "html.parser") -> dict[str, t.Union[list[str], list[dict[str, str]]]]:
    soup: bs4.BeautifulSoup = get_soup(url=url, headers=headers, parser=parser)
    
    ## Extract UA category table
    ua_category_tbl: bs4.Tag = soup.find("table", attrs={"id": "auswahl"})
    
    ## Extract vertical columns with categories
    ua_tbl_cols: list[bs4.Tag] = ua_category_tbl.find_all("td")
    
    ## Extract category tags
    ua_category_tags: list[bs4.Tag] = []
    links: list[str] = []
    for col in ua_tbl_cols:
        ## Extract all category links
        a_hrefs: list[bs4.Tag] = col.find_all("a")
        ## Add link tags to list
        ua_category_tags = ua_category_tags + a_hrefs
        
        a_href_links: list[dict[str, str]] = []
        for _a in a_hrefs:
            ## Format category name & link
            _a_name = _a.text.strip(" ")
            _a_link = f"{UASTRING_BASE_URL}{_a['href']}".strip(" ")
            log.debug(f"Link name: {_a_name}, Link: {_a_link}")
            
            if _a_name.endswith("user agents strings -->>"):
                log.warning(f"Found link to more UAs: {_a_name}: {_a_link}")
            
            a_href_links.append({"name": _a_name, "link": _a_link})
        
        links = links + a_href_links
    
    return_obj: dict[str, t.Union[list[str], list[dict[str, str]]]] = {"links": links, "extracted_tags": ua_category_tags}
    
    return return_obj


def crawl_ua_categories(headers: dict | None = None, parser: str = "html.parser", request_sleep: int = 5, save_html: bool = False, html_output_dir: t.Union[str, Path] = "./html_cache", save_json: bool = False, json_output_dir: t.Union[str, Path] = "./json_cache"):
    ua_categories: dict[str, list[str] | list[dict[str, str]]] = scrape_ua_categories(headers=headers, parser=parser)
    categories = ua_categories["links"]
    category_uas: list = []
    
    if save_json:
        if not Path(str(json_output_dir)).exists():
            log.warning(f"JSON output path '{json_output_dir}' does not exist. Creating.")
            Path(str(json_output_dir)).mkdir(parents=True, exist_ok=True)
    
    if save_html:
        if not Path(str(html_output_dir)).exists():
            log.warning(f"HTML output path '{html_output_dir}' does not exist. Creating.")
            Path(str(html_output_dir)).mkdir(parents=True, exist_ok=True)
            
    
    log.info(f"Crawling [{len(categories)}] User Agent category/ies")
    for category in categories:
        log.debug(category)
        log.info(f"Getting BeautifulSoup for URL: {category['link']}")
        try:
            category_soup = get_soup(url=category["link"])
        except Exception as exc:
            msg= f"({type(exc)}) Error scraping page '{category['link']}'. Details: {exc}"
            log.error(f"{msg}")
            continue

        log.info(f"Extracting UA strings from category '{category['name']}'")
        try:
            ua_strings: list[str] = extract_ua_strings(soup=category_soup)
            category_uas.append({"client": category["name"], "user_agents": ua_strings})
        except Exception as exc:
            msg = f"({type(exc)}) Error extracting UA string(s) from category '{category['name']}'. Details: {exc}"
            log.error(msg)
            
            raise exc
        
        if save_json:
            log.info(f"Saving '{category['name']}' UA string(s) to file '{json_output_dir}/{category['name']}_uas.json")
            with open(f"{json_output_dir}/{category['name']}_uas.json", "w") as f:
                _data = json.dumps(category_uas, indent=4, sort_keys=True, default=str)
                f.write(_data)

        if request_sleep:
            print(f"Sleeping for {request_sleep} second(s)...")
            time.sleep(request_sleep)
            
    if save_json:
        log.info(f"Saving scraped JSON data to: {json_output_dir}")
        _data = json.dumps(category_uas, indent=4, sort_keys=True, default=str)
        
        try:
            with open(f"{json_output_dir}/categorized_uas.json", "w") as f:
                f.write(_data)
        except Exception as exc:
            msg = f"({type(exc)}) Error saving scraped data to JSON file '{json_output_dir}/categorized_uas.json"
            log.error(msg)
    
    log.info(f"Scraped [{len(category_uas)}] UA string(s)")
    return category_uas
