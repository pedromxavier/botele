import json
import marshal
import argparse
import traceback
from pathlib import Path

from pyckage.pyckagelib import PackageData
from cstream import stderr

from ..botele import Botele, BoteleMeta
from ..botlib import get_bot_context


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

    if args.bot not in bots_data:
        stderr[0] << (
            f"Error: Unknown bot `{args.bot}`. "
            + "Run `botele list` to see available bots."
        )
        return 1

    bot_data: dict = bots_data[args.bot]

    bot_path = Path(bot_data["path"])

    if not bot_path.exists() or not bot_path.is_dir():
        stderr[0] << (
            f"Error: Bot directory `{bot_path}` is missing. " + "Try running `botele install`"
        )
        return 1

    bot_data_path = bot_path.joinpath("botdata")

    if not bot_path.exists() or not bot_path.is_dir():
        stderr[0] << (
            f"Error: Bot data directory is missing. " + "Try running `botele install`"
        )
        return 1

    bot_source = Path(bot_data["source"])

    if not bot_source.exists() or not bot_source.is_file():
        stderr[0] << (
            f"Error: Bot source file is missing. " + "Try running `botele install`"
        )
        return 1

    with open(bot_source, mode="rb") as file:
        code = marshal.load(file)

    context: dict = get_bot_context(bot_data_path)

    try:
        exec(code, context)
    except:
        stderr[0] << "There are errors in the bot source code:"
        stderr[0] << traceback.format_exc()
        return 1

    token: str = bot_data["token"]
    bot_name: str = bot_data["name"]

    Bot = BoteleMeta.__bots__[bot_name]
    bot = Bot(name=bot_name, token=token, path=bot_path)
    bot.setup()
    bot.run()
    return 0