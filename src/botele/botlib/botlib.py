## Standard Library
import os
import re
import sys
import site
import json
import pickle
import psutil
import random
from pathlib import Path
from functools import wraps

from pyckage.pyckagelib import PackageData


def start_logging(level: int=None):
    global logging
    import logging

    level = logging.DEBUG if logging is None else level

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
    )


def shuffled(x: list) -> list:
    """Returns shuffled copy of a list.

    Parameters
    ----------
    x: list
        List to be shuffled

    Returns
    -------
    list
        Shuffled list
    """
    y = list(x)
    random.shuffle(y)
    return y


def root_open(root: str) -> callable:
    """
    Parameters
    ----------
    root : str
        Root path for open() reference

    Returns
    -------
    callable
        open(...) function rooted at `root` path.
    """

    root_path = Path(root).absolute()

    if not root_path.exists() or not root_path.is_dir():
        raise OSError(f"Invalid folder path `{root_path}`.")

    @wraps(open)
    def __open(path: str, *args, **kwargs):
        open_path = root_path.joinpath(path)
        try:
            return open(open_path, *args, **kwargs)
        except FileNotFoundError:
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        except PermissionError:
            raise PermissionError(f"[Errno 13] Permission denied: '{path}'")


def get_bot_context(root: str = None) -> dict:
    """
    Parameters
    ----------
    root : str
        Root path for open() reference

    Returns
    -------
    dict
        global context dictionary
    """
    if root is None:
        return {}
    else:
        return {"__builtins__": {**__builtins__, "open": root_open(root=root)}}


def file_name(__file__: str) -> str:
    """
    Returns
    -------
    str
        Current script file name (without .py, .pyw extensions)
    """
    return Path(__file__).stem


def get_bot_data(bot_key: str) -> dict:
    """"""
    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")

    data_path = package_path.joinpath(".botele-bots")

    if not data_path.exists():
        return None

    with open(data_path, mode='r') as file:
        bots_data = json.load(file)

    if bot_key not in bots_data:
        return None
    else:
        return bots_data[bot_key]

def set_bot_data(bot_key: str, bot_data: dict) -> dict:
    """"""
    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")
    
    data_path = package_path.joinpath(".botele-bots")

    if data_path.exists():
        with open(data_path, mode='r') as file:
            bots_data = json.load(file)
    else:
        bots_data = {}
    
    bots_data[bot_key] = bot_data

    with open(data_path, mode='w') as file:
        json.dump(bots_data, file)