import json
import argparse

from pyckage.pyckagelib import PackageData
from cstream import stdout

def list_(args: argparse.Namespace):
    
    package_data = PackageData('botele')

    with package_data.open_data('.botele-bots') as file:
        bots_data: dict = json.load(file)

    if bots_data:
        stdout[0] << 'Available bots:'
        for i, bot_key in enumerate(bots_data):
            stdout[0] << f"\t{i:<2d}. {bot_key}"
    else:
        stdout[0] << "No bots available."