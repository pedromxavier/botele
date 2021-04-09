# Standard Library
import os
import json
import argparse
import traceback
import multiprocessing as mp
from pathlib import Path

# Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr, stdwar, stdout

# Local
from .list_ import list_bots
from ..botlib import ProcessData

def kill(args: argparse.Namespace) -> int:
    """Sends SIGINT to given bot processes.
    Parameters
    ----------
    args: argparse.Namespace
        Command-line arguments:
        .bot: list
            List of strings with bot identifiers.
        .all: bool
            Wether to kill all alive bots or not.
    """
    args.bot: list
    args.all: bool

    if bool(args.bot) and args.all:
        stderr[0] << "Error: '--all' can't be used with any bot identifier as argument."
        return 1
    
    # Retrieve Package Data Environment
    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")
    process_data = ProcessData(package_path.joinpath('pid'))

    if args.all:
        for pkey in process_data.get_alive_process_keys():
            process_data.kill_process(pkey)
        return 0

    bot_keys = set(list_bots())

    for pkey in args.bot:
        if pkey not in bot_keys:
            stderr[0] << f"Invalid bot identifier '{pkey}'."
        elif not process_data.is_alive(pkey):
            stdwar[0] << f"Actually, bot '{pkey}' is not alive."
        else:
            process_data.kill_process(pkey)

    return 0