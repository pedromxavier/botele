import os
import json
import argparse
from pathlib import Path

## Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr

def make(args: argparse.Namespace) -> int:
    """
    """
    if args.path is None:
        path = Path.cwd()
    else:
        if os.path.exists(args.path):
            path = Path(args.path).absolute()
        else:
            stderr[0] << f"Invalid destination folder: `{args.path}`."
            return 1

    bot_path = path.joinpath('.botele')

    if not bot_path.exists():
        stderr[0] << f"There is an no bot environment here. Use `botele setup` to begin current installation."
        return 1

    # Get bot info
    with open(bot_path, mode='r') as file:
        bot_data: dict = json.load(file)

    token_path = Path(bot_data['token_path'])

    if token_path is None:
        stderr[0] << f"No bot token defined. Place it in a `*.token` file."
        return 1
    
    with open(token_path, mode='r') as file:
        token: str = file.read()
    
    package_data = PackageData('botele')
    package_path = package_data.get_data_path('')

    package_bots_path = package_path.joinpath('.botele-bots')
