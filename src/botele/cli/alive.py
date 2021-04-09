# Standard Library
import json
import argparse
import traceback
import multiprocessing as mp
from pathlib import Path

# Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr, stdwar, stdout

from ..botlib import ProcessData

def alive(args: argparse.Namespace) -> int:
    """"""
    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")
    process_data = ProcessData(package_path.joinpath("pid"))

    bot_keys = list(process_data.get_alive_process_keys())

    if bot_keys:
        stdout[0] << "Alive bots:"
        for i, bot_key in enumerate(bot_keys, start=1):
            stdout[0] << f"\t{i:>2d}. {bot_key}"
    else:
        stdout[0] << "No bots alive."

    return 0