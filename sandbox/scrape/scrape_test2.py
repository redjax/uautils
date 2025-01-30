from loguru import logger as log

from pathlib import Path
import typing as t
import json

from domain import uastring_domain

import settings
import setup
import http_lib

import bs4

html_cache_dir = Path("sandbox/scrape/html_cache")

if not html_cache_dir.exists():
    html_cache_dir.mkdir(parents=True, exist_ok=True)


def main(urls: list[dict[str,str]], html_cache_dir: str = html_cache_dir):
    log.debug(f"URLs dict: {urls}")
    
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    log.debug(f"Headers: {headers}")
    
    all_user_agents: list[dict[str, t.Union[str, dict[str, str]]]] = []
    soups: list[bs4.BeautifulSoup] = []
    
    for ua_dict in urls:
        log.info(f"Scraping {ua_dict['category']} UA strings")
        
        ua_category = ua_dict["category"]
        ua_page_url = ua_dict["url"]        
        log.debug(f"UA category: {ua_category}, URL: {ua_page_url}")
        
        req = http_lib.build_request(url=ua_page_url, headers=headers)
        
        with http_lib.get_http_controller(cache_ttl=900) as http_ctl:
            res = http_ctl.send_request(req)
            res.raise_for_status
            
        if not res.status_code == 200:
            log.warning(f"Non-200 response code: [{res.status_code}: {res.reason_phrase}]: {res.text}")
            continue
        
        log.info(f"Response: [{res.status_code}: {res.reason_phrase}]")
        
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        soups.append(soup)
        
        save_html_file = f"{html_cache_dir}/{ua_page_url.replace('http://', '').replace('https://', '').replace('/', '__').replace('%', '--')}.html"
        
        ## Save scraped page
        with open(save_html_file, "w") as f:
            f.write(soup.prettify())
            
        ## Extract the 'liste' div that has all the user agents
        list_div: bs4.Tag = soup.find("div", attrs={"id": "liste"})
        # log.debug(f"UA list div ({type(list_div)}): {list_div}")
        
        ## Extract individual <ul> lists on page
        ua_lists: bs4.ResultSet[t.Any] = list_div.find_all("ul")
        # log.debug(f"UA lists ({type(ua_lists)}): {ua_lists}")
        
        ## Loop over lists of UA strings
        for ua_list in ua_lists:
            log.debug("Extracting <a> tags from soup")
            ## Grab all links
            links = ua_list.find_all("a")
            # log.debug(f"Found links ({type(links)}): {links}")
            
            log.debug("Creating list of UA strings from soup")
            link_texts = [l.text for l in links]
            
            log.debug(f"Create results object, prettify 'soup' objects")
            ## Add links to results
            result = {"category": ua_category, "user_agents": link_texts, "url": ua_page_url}
            log.debug(f"Append user agent scrape results to list")
            all_user_agents.append(result)
            
    log.info(f"Found [{len(all_user_agents)}] UA string(s)")
    # log.debug(f"Example UA strings: {all_user_agents[:5]}")
    
    log.info(f"Saving to ./sandbox/scrape/all_ua_strings.json")
    try:
        with open("./sandbox/scrape/all_ua_strings.json", "w") as f:
            data = json.dumps(all_user_agents, sort_keys=True, indent=4, default=str)
            f.write(data)
    except Exception as exc:
        msg = f"({type(exc)}) Error writing to file './sandbox/scrape/all_ua_strings.json'. Details: {exc}"
        log.error(msg)
        raise

    
if __name__ == "__main__":
    ua_urls: list[dict[str, str]] = [
        {"category": "desktop", "url": "https://www.useragentstring.com/pages/Browserlist/"},
        {"category": "mobile", "url": "https://www.useragentstring.com/pages/Mobile%20Browserlist/"},
        {"category": "console", "url": "https://www.useragentstring.com/pages/Consolelist/"}
    ]
    
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main(urls=ua_urls)