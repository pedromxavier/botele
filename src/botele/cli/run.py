# Standard Library
import json
import argparse
import traceback
import subprocess as sp
import multiprocessing as mp
from pathlib import Path

# Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr, stdwar

from .list_ import list_bots
from ..botlib import get_bot_data, ProcessData

def run(args: argparse.Namespace) -> int:
    """
    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments:
        .bot: list
            List of strings with bot identifiers.
        .all: bool
            Wether to run all alive bots or not.
    """
    args.bot: list
    args.all: bool

    if bool(args.bot) and args.all:
        stderr[0] << "Error: '--all' can't be used with any bot identifier as argument."
        return 1

    if args.all:
        bot_keys = set(list_bots())
    elif bool(args.bot):
        bot_keys = set(args.bot)
    else:
        stderr[0] << "Not bot identifier provided."
        return 1

    for bot_key in list(bot_keys):
        if not check_bot(bot_key):
            bot_keys.discard(bot_key)

    if not bool(bot_keys):
        return 0

    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")
    process_path = package_path.joinpath("pid")
    process_data = ProcessData(process_path)

    if args.wait:
        processes = []
        for bot_key in list(bot_keys):
            process = mp.Process(target=run_bot, args=(bot_key,))
            processes.append((bot_key, process))
        for pkey, process in processes:
            process.start()
            process_data.dump_data(pkey, process.pid)
        for _, process in processes:
            process.join()
    return 0

def check_bot(bot_key: str) -> bool:
    """"""

    bot_data: dict = get_bot_data(bot_key)

    if bot_data is None:
        stderr[0] << f"Bot '{bot_key}' is not properly installed."
        return False

    bot_path: Path = Path(bot_data["path"])

    if not bot_path.exists() or not bot_path.is_dir():
        stderr[0] << (
            f"Error: Bot directory `{bot_path}` is missing. "
            + "Try running `botele install`"
        )
        return False

    bot_data_path = bot_path.joinpath("botdata")

    if not bot_data_path.exists() or not bot_data_path.is_dir():
        stderr[0] << (
            f"Error: Bot data directory `{bot_data_path.name}` is missing. "
            + "Try running `botele install`"
        )
        return False

    bot_source = Path(bot_data["source"])

    if not bot_source.exists() or not bot_source.is_file():
        stderr[0] << (
            f"Error: Bot source file `{bot_source.name}` is missing. "
            + "Try running `botele install`"
        )
        return False

    return True


def run_bot(bot_key: str) -> int:
    """"""
    import marshal
    from pathlib import Path
    from ..botele import Botele, BoteleMeta
    from ..botlib import get_bot_context, get_bot_data

    bot_data: dict = get_bot_data(bot_key)

    bot_source = Path(bot_data["source"])

    with open(bot_source, mode="rb") as file:
        code = marshal.load(file)

    bot_path = Path(bot_data["path"])

    bot_data_path = bot_path.joinpath("botdata")

    # This was previously verified by calling
    # `botele make`.
    exec(code, get_bot_context(bot_data_path))

    bot_token: str = bot_data["token"]
    bot_name: str = bot_data["name"]

    # Get Bot Class
    Bot = BoteleMeta.__bots__[bot_name]

    bot = Bot(name=bot_name, token=bot_token, path=bot_path)
    bot.setup()

    # Here we go!
    bot.run()

    return 0