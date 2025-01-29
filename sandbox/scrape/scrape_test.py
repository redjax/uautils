from loguru import logger as log

from pathlib import Path
import typing as t

import settings
import setup
import http_lib

import bs4

html_cache_dir = Path("sandbox/scrape/html_cache")

if not html_cache_dir.exists():
    html_cache_dir.mkdir(parents=True, exist_ok=True)


def main(urls: dict[str, dict[str, str]], html_cache_dir: str = html_cache_dir):
    log.debug(f"URLs dict: {urls}")
    
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    log.debug(f"Headers: {headers}")

    soups: list[bs4.BeautifulSoup] = []
    user_agents: list[str] = []

    for ua_dict_name in urls:
        log.info(f"Scraping {ua_dict_name} User Agent strings")
        ua_dict = urls[ua_dict_name]
        log.debug(f"User Agent dict: {ua_dict}")
        log.debug(f"Keys: {ua_dict.keys()}")
        req = http_lib.build_request(url=ua_dict["url"], headers=headers)
    
        with http_lib.get_http_controller(cache_ttl=900) as http_ctl:
            res = http_ctl.send_request(req)
            res.raise_for_status()
            
        if not res.status_code == 200:
            log.warning(f"Non-200 response code: [{res.status_code}: {res.reason_phrase}]: {res.text}")
            return
        else:
            log.info(f"Response: [{res.status_code}: {res.reason_phrase}]")
            
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        # log.info(f"Soup type: {type(soup)}")
        # log.info(f"Soup: {soup.prettify()}")
        
        with open(f"{html_cache_dir}/{ua_dict['url'].replace('http://', '').replace('https://', '').replace('/', '__').replace('%', '--')}.html", "w") as f:
            f.write(soup.prettify())
        
        list_div: bs4.Tag = soup.find("div", attrs={"id": "liste"})
        # log.debug(f"UA list div ({type(list_div)}): {list_div}")
        
        ua_lists: bs4.ResultSet[t.Any] = list_div.find_all("ul")
        # log.debug(f"UA lists ({type(ua_lists)}): {ua_lists}")
        
        for ua_list in ua_lists:
            links = ua_list.find_all("a")
            # log.debug(f"Found links ({type(links)}): {links}")
            
            for link in links:
                user_agents.append(link.text)
                
    log.info(f"Retrieved [{len(user_agents)}] User Agent strings")
    log.debug(f"Example UAs: {user_agents[:5]}")
        
          
    
    
if __name__ == "__main__":
    ua_urls: dict = {
        "browsers": {"name": "browser_uas","url": "https://www.useragentstring.com/pages/Browserlist/"},
        "mobile": {"name": "mobile_browser_uas", "url": "https://www.useragentstring.com/pages/Mobile%20Browserlist/"},
        "console": {"name": "console_uas", "url": "https://www.useragentstring.com/pages/Consolelist/"}
    }
    
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"), colorize=True)
    main(urls=ua_urls)
