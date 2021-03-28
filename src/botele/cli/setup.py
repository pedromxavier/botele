import json
import argparse
from pathlib import Path

from cstream import stderr, stdwar

def setup(args: argparse.Namespace) -> int:
    if args.path is None:
        path = Path.cwd()
    else:
        path = Path(args.path)

    if not path.exists() or not path.is_dir():
        stderr[0] << f"Invalid directory `{path}`. Aborted."
        return 1

    if next(path.glob('*'), None) is not None:
        stdwar[0] << f"The `botele setup` command should be used in an empty directory. Pay attention to unwanted behavior."

    # Data folder
    path.joinpath("botdata").mkdir(exist_ok=True)

    # Files
    if args.name is None:
        bot_name: str = path.stem
    else:
        bot_name: str = args.name

    # Create files
    path.joinpath(f"{bot_name}.token").touch(exist_ok=True)
    path.joinpath(f"{bot_name}.py").touch(exist_ok=True)

    path.joinpath(".bot").touch(exist_ok=True)

    bot_data: dict = {
        'name': bot_name,
        'path': None,
        'token': None,
        'source': None,
    }

    with open(path.joinpath(".bot"), mode='w') as file:
        json.dump(bot_data, file)

    return 0