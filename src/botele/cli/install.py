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

    local_bot_path = path.joinpath(".bot").absolute()

    if not local_bot_path.exists():
        stderr[0] << (
            "Path Error: There is no bot environment here. "
            + "Use `botele setup` to begin current installation."
        )
        return 1

    # Get bot info
    with open(local_bot_path, mode="r", encoding='utf-8') as file:
        bot_data: dict = json.load(file)

    package_data = PackageData("botele")
    package_path = package_data.get_data_path("")

    bots_dir_path = package_path.joinpath("bots")

    if not bots_dir_path.exists():
        bots_dir_path.mkdir(exist_ok=False)

    ## Bot install folder
    bot_name: str = bot_data["name"]

    bot_dir_path = bots_dir_path.joinpath(bot_name)

    if bot_dir_path.exists():
        stdwar[0] << f"Warning: Clearing content from `{bot_dir_path}`."
        shutil.rmtree(bot_dir_path)

    bot_dir_path.mkdir(exist_ok=False)

    ## Bot local source path
    local_src_path = Path(bot_data["source"])

    if not local_src_path.exists():
        stderr[0] << (
            f"Path Error: Compiled source `{local_src_path}` is missing. "
            + "Try running `botele make`."
        )
        return 1

    ## Bot local data path.
    data_path = path.joinpath("botdata")

    if not data_path.exists():
        stdwar[0] << f"Warning: No `botdata` folder found."
        data_path = None
    elif not data_path.is_dir():
        stderr[0] << f"Error: `botdata` must be a directory."
        return 1

    ## Bot install source path
    install_src_path = bot_dir_path.joinpath(local_src_path.name)

    shutil.copy(local_src_path, install_src_path)

    install_data_path = bot_dir_path.joinpath("botdata")

    if data_path is not None:
        shutil.copytree(data_path, install_data_path)
    else:
        install_data_path.mkdir()

    bots_data_path = package_path.joinpath(".botele-bots")

    if not bots_data_path.exists():
        stderr[0] << "Fatal Error: Internal files missing. Try reinstalling botele."
        return 2

    bot_data.update(
        {
            "path": str(bot_dir_path),
            "source": str(install_src_path),
        }
    )

    with open(bots_data_path, mode="r", encoding='utf-8') as file:
        bots_data: dict = json.load(file)

    bots_data[bot_name] = bot_data

    with open(bots_data_path, mode="w", encoding='utf-8') as file:
        json.dump(bots_data, file)

    return 0