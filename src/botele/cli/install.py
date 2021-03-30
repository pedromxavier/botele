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
    with open(bot_path, mode="r") as file:
        bot_data: dict = json.load(file)

    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")

    bots_dir_path = package_path.joinpath("bots")

    if not bots_dir_path.exists():
        bots_dir_path.mkdir(exist_ok=False)

    bot_name: str = bot_data["name"]

    bot_dir_path = bots_dir_path.joinpath(bot_name)

    if bot_dir_path.exists():
        stdwar[0] << f"Warning: Clearing content from `{bot_dir_path}`."
        shutil.rmtree(bot_dir_path)

    bot_dir_path.mkdir(exist_ok=False)

    src_path = Path(bot_data["source"])

    if not src_path.exists():
        stderr[0] << (
            f"Path Error: Compiled source `{src_path}` is missing. "
            + "Try running `botele make`."
        )
        return 1

    data_path = path.joinpath("botdata")

    if not data_path.exists():
        stdwar[0] << f"Warning: No `botdata` folder found."
        data_path = None
    elif not data_path.is_dir():
        stderr[0] << f"Path Error: `botdata` must be a directory."
        return 1

    shutil.copy(src_path, bot_dir_path.joinpath(src_path.name))

    if data_path is not None:
        shutil.copytree(data_path, bot_dir_path.joinpath("botdata"))

    bots_file_path = package_path.joinpath(".botele-bots")

    if not bots_file_path.exists():
        stderr[0] << "Fatal Error: Internal files missing. Try reinstalling botele."
        return 2

    with open(bots_file_path, mode="r") as file:
        bots: dict = json.load(file)

    bots[bot_name] = bot_data

    with open(bots_file_path, mode="w") as file:
        json.dump(bots, file)

    return 0