from __future__ import annotations

import typing as t
import re
from pathlib import Path
from loguru import logger as log

def sanitize_filename(filename: str, space_replacement: str = "_", unsafe_char_replacement: str = "-") -> str:
    """Sanitizes a filename to be safe for all OS paths by replacing unsafe characters.
    
    Params:
        filename (str): The original filename.
        space_replacement (str): Replacement for spaces. Default is "_".
        unsafe_char_replacement (str): Replacement for other unsafe characters. Default is "-".
        
    Returns:
        str: The sanitized filename.

    """
    ## Characters that are generally unsafe for filenames
    unsafe_characters = r'[<>:"/\\|?*]'
    
    ## Replace spaces with the defined space replacement
    filename = filename.replace(" ", space_replacement)
    
    ## Replace other unsafe characters with the defined unsafe character replacement
    filename = re.sub(unsafe_characters, unsafe_char_replacement, filename)
    
    ## Strip leading and trailing whitespace or replacement characters
    filename = filename.strip(unsafe_char_replacement + space_replacement)
    
    return filename


def path_exists(p: t.Union[str, Path]) -> bool:
    """Check if a path exists.
    
    Params:
        p (str | Path): Path to check.
    
    Returns:
        (bool): True if path exists, False otherwise.
    
    """
    p: Path = Path(str(p)).expanduser().resolve() if "~" in p else Path(str(p)).resolve()
    
    return p.exists()


def read_file(file_path: t.Union[str, Path], mode: str = "r") -> t.Any:
    """Reads a file and returns its contents as a list of lines.
    
    Params:
        file_path (str | Path): Path to the file to read.
        mode (str): Mode to open the file in. Options: ['r', 'r+', 'rb', 'rb+']
    
    Returns:
        (list): List of lines in the file.

    """
    if mode not in ["r", "r+", "rb", "rb+"]:
        raise ValueError(f"Invalid mode: '{mode}'. Must be one of: ['r', 'r+', 'rb', 'rb+']")

    file_path = Path(str(file_path)).expanduser().resolve() if "~" in str(file_path) else Path(str(file_path)).resolve()
    
    log.info(f"Reading file '{file_path}'")
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
    except PermissionError:
        log.error(f"Permission denied reading file '{file_path}'.")
        raise
    except FileNotFoundError:
        log.error(f"File '{file_path}' not found.")
        raise
    except Exception as exc:
        msg = f"({type(exc).__name__}) Unhandled exception reading file '{file_path}': {exc}"
        log.error(msg)
        raise
    
    return lines
