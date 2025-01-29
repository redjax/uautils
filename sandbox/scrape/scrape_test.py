from loguru import logger as log

from pathlib import Path
import typing as t

import settings
import setup
import http_lib

def main(url: str):
    log.debug(f"Requesting UA string home: {url}")

    
if __name__ == "__main__":
    ua_string_home = "https://www.useragentstring.com/pages/useragentstring.php"
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO", colorize=True))
    main(url=ua_string_home)
