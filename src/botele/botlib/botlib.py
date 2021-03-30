## Standard Library
import os
import sys
import site
import random
import pickle
import logging
from pathlib import Path
from functools import wraps


def start_logging(level=logging.DEBUG):
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

__all__ = ['root_open', 'shuffled', 'start_logging']