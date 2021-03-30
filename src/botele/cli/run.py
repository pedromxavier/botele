import json
import marshal
import argparse

from pyckage.pyckagelib import PackageData
from cstream import stderr

from ..botele import Botele
from ..botlib import root_open


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

    with open(bot_data['source'], mode='rb') as file:
        code = marshal.load(file)

    context: dict = {'__builtins__': {**__builtins__, 'open': root_open(root=bot_data_path)}}


    bot.run(token=token)

    return 0