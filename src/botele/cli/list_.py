import json
import argparse

from pyckage.pyckagelib import PackageData
from cstream import stdout

def list_bots() -> list:
    package_data = PackageData("botele")

    with package_data.open_data(".botele-bots") as file:
        bots_data: dict = json.load(file)

    return list(bots_data.keys())

def list_(args: argparse.Namespace) -> int:
    """"""
    bot_keys = list_bots()

    if bot_keys:
        stdout[0] << "Available bots:"
        for i, bot_key in enumerate(bot_keys, start=1):
            stdout[0] << f"\t{i:>2d}. {bot_key}"
    else:
        stdout[0] << "No bots available."

    return 0