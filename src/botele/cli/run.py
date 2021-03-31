import json
import argparse
import traceback
import multiprocessing as mp
from pathlib import Path

from pyckage.pyckagelib import PackageData
from cstream import stderr


def run(args: argparse.Namespace) -> int:
    """"""

    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")

    bots_path = package_path.joinpath(".botele-bots")

    if not bots_path.exists():
        stderr[0] << "Fatal Error: Bots index missing. Try reinstalling botele."
        return 1

    with open(bots_path, mode="r") as file:
        bots_data: dict = json.load(file)

    problems = False

    bot_name: str
    for bot_name in args.bot:
        if bot_name not in bots_data:
            stderr[0] << f"Error: Unknown bot `{bot_name}`."
            problems = True

    if problems:
        stderr[0] << "Run `botele list` to see available bots."
        return 1

    bots = []

    for bot_name in args.bot:
        bot_data: dict = bots_data[bot_name]
        if not check_bot(bot_data):
            stderr[0] << f"There are problems with {bot_name}'s installation."
            problems = True
        elif not problems:
            bots.append(bot_data)
        else:
            continue

    if problems:
        return 1

    # Here things get interesting. Multiprocessing arises!
    p = [mp.Process(target=check_bot, args=(bot_data,)) for bot_data in bots]


def check_bot(bot_data: dict) -> bool:
    """"""

    bot_path = Path(bot_data["path"])

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


def run_bot(bot_data: dict):
    import marshal
    from ..botele import Botele, BoteleMeta
    from ..botlib import get_bot_context

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