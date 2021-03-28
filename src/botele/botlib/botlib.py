## Standard Library
import os
import sys
import site
import random
import pickle
import logging


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


def load_token(path: str) -> str:
    """"""
    if not path.endswith(".token"):
        raise ValueError(f"Invalid token file path: `{path}`.")

    with open(path, mode="r") as file:
        return file.read()