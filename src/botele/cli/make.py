import os
import re
import json
import argparse
from pathlib import Path

## Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr

RE_TOKEN = re.compile(r'^[0-9]{9}\:[a-zA-Z0-9_-]{35}$', re.UNICODE)

def make(args: argparse.Namespace) -> int:
    """
    """
    if args.path is None:
        path = Path.cwd()
    else:
        path = Path(args.path)
        if not path.exists():
            stderr[0] << f"Invalid directory `{args.path}`."
            return 1
        else:
            path = Path(args.path).absolute()

    bot_path = path.joinpath('.bot')

    if not bot_path.exists():
        stderr[0] << f"There is no bot environment here. Use `botele setup` to begin current installation."
        return 1

    # Get bot info
    with open(bot_path, mode='r') as file:
        bot_data: dict = json.load(file)

    bot_name: str = bot_data['name']

    # Token
    token_path = path.joinpath(f'{bot_name}.token')

    if not token_path.exists():
        stderr[0] << f"No token file `{bot_name}.token`."
        return 1

    with open(token_path, mode='r') as file:
        token: str = file.read().strip('\t\n ')
    
    if RE_TOKEN.match(token) is None:
        stderr[0] << f"Invalid token at `{bot_name}.token`."
        return 1

    # Source
    source_path = path.joinpath(f'{bot_name}.py')

    if not source_path.exists():
        stderr[0] << f"No bot source code file `{bot_name}.py`."
        return 1
    
    



    if token is None:
        stderr[0] << f"No bot token defined. Place it in a `*.token` file."
        return 1
    
    with open(token_path, mode='r') as file:
        token: str = file.read()
    
    package_data = PackageData('botele')
    package_path = package_data.get_data_path('')

    package_bots_path = package_path.joinpath('.botele-bots')
