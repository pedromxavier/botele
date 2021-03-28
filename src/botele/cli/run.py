import json
import argparse

from pyckage.pyckagelib import PackageData
from cstream import stderr

from ..botele import Botele

def run(args: argparse.Namespace):
    """"""

    package_data = PackageData('botele')
    package_path = package_data.get_data_path('')

    bots_path = package_path.joinpath('.botele-bots')

    if not bots_path.exists():
        raise FileNotFoundError("Installation Error, bots index missing.")

    with open(bots_path, mode='r') as file:
        bots_data: dict = json.load(file)

    if args.bot not in bots_data:
        stderr[0] << f"Unknown bot `{args.bot}`. Run `botele list` to see available bots."
        return
        
    bot = Botele.load(bots_data[args.bot])
    bot.setup()
    bot.run()