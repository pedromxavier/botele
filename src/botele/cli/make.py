import os
import re
import json
import marshal
import argparse
import traceback
from pathlib import Path

## Third-Party
from pyckage.pyckagelib import PackageData
from cstream import stderr, stdwar

## Local
from ..botele import Botele
from ..botlib import get_bot_context

RE_TOKEN = re.compile(r"^[0-9]{10}\:[a-zA-Z0-9_-]{35}$", re.UNICODE)


def make(args: argparse.Namespace) -> int:
    """"""
    if args.path is None:
        path = Path.cwd()
    else:
        path = Path(args.path)
        if not path.exists():
            stderr[0] << f"Invalid directory `{args.path}`."
            return 1
        else:
            path = Path(args.path).absolute()

    bot_data_path = path.joinpath(".bot")

    if not bot_data_path.exists():
        stderr[0] << (
            f"There is no bot environment here. Use `botele setup` to begin current installation."
        )
        return 1

    # Get bot info
    with open(bot_data_path, mode="r") as file:
        bot_data: dict = json.load(file)

    bot_name: str = bot_data["name"]

    # Token
    token_path = path.joinpath(f"{bot_name}.token")

    if not token_path.exists():
        stderr[0] << f"Error: No token file `{bot_name}.token`."
        return 1

    with open(token_path, mode="r") as file:
        token: str = file.read().strip("\t\n ")

    if RE_TOKEN.match(token) is None:
        stderr[0] << f"Error: Invalid token at `{bot_name}.token`."
        return 1

    # Source
    source_path = path.joinpath(f"{bot_name}.py")

    if not source_path.exists():
        stderr[0] << f"Error: No bot source code file `{bot_name}.py`."
        return 1

    with open(source_path, mode="r", encoding="utf-8") as file:
        source: str = file.read()

    code = compile(source, filename=source_path.name, mode="exec")

    context = get_bot_context(root=None)

    try:
        exec(code, context)
    except:
        stderr[0] << "There are errors in the bot source code:"
        stderr[0] << traceback.format_exc()
        return 1

    bots = {
        key: item
        for key, item in context.items()
        if isinstance(item, type) and issubclass(item, Botele) and item is not Botele
    }

    if len(bots) == 0:
        stderr[0] << f"Error: No bot defined at `{bot_name}.py`."
        return 1
    elif len(bots) >= 2:
        stderr[0] << f"Error: Multiple bots defined at `{bot_name}.py`."
        return 1

    BotName, BotClass = bots.popitem()

    if BotName.lower() != bot_name:
        stderr[0] << f"Bot Class name must be equal to the bot name, ignoring case."
        return 1

    if BotClass.error_handler is None:
        stdwar[0] << f"No Error Handler defined for bot `{BotName}`."

    pyc_path = path.joinpath(f"{bot_name}.pyc")
    pyc_path.touch(exist_ok=True)

    with open(pyc_path, mode="wb") as file:
        marshal.dump(code, file)

    bot_data.update(
        {
            "path": str(path),
            "token": token,
            "source": str(pyc_path),
        }
    )

    with open(bot_data_path, mode="w", encoding="utf-8") as file:
        json.dump(bot_data, file)

    return 0