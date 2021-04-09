import json
import shutil
import argparse
from pathlib import Path

from pyckage.pyckagelib import PackageData
from cstream import stderr, stdwar


def install(args: argparse.Namespace) -> int:
    """"""
    if args.path is None:
        path = Path.cwd()
    else:
        path = Path(args.path)
        if not path.exists():
            stderr[0] << f"Path Error: Invalid directory `{args.path}`."
            return 1
        else:
            path = Path(args.path).absolute()

    bot_path = path.joinpath(".bot").absolute()

    if not bot_path.exists():
        stderr[0] << (
            "Path Error: There is no bot environment here. "
            + "Use `botele setup` to begin current installation."
        )
        return 1

    # Get bot info
    with open(bot_path, mode="r", encoding='utf-8') as file:
        bot_data: dict = json.load(file)

    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")

    bots_dir_path = package_path.joinpath("bots")
    bots_conf_path = package_path.joinpath(".botele-config")

    raise NotImplementedError("IMPLEMENT ME PLEASE.")