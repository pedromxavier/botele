import argparse

from .run import run
from .make import make
from .list import list_
from .setup import setup

from cstream import stderr

def main():
    """"""

    params = {"description": __doc__}

    parser = argparse.ArgumentParser(**params)
    parser.add_argument(
        "-v",
        "--verbose",
        choices=range(3),
        type=int,
        action="store",
        default=0,
        help="Output verbosity.",
    )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "bot", dest="bot", type=str, action="store", help="Bot identifier"
    )
    run_parser.set_defaults(func=run)

    setup_parser = subparsers.add_parser("setup")
    setup_parser.add_argument("path", type=str, action="store", help="Bot folder path")
    setup_parser.add_argument(
        "-n",
        "--name",
        type=str,
        action="store",
        help="Bot identifier (defaults to directory name)",
    )
    setup_parser.set_defaults(func=setup)

    make_parser = subparsers.add_parser("make")
    make_parser.add_argument("path", type=str, action="store", help="Bot folder path")
    make_parser.set_defaults(func=make)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_)

    args = parser.parse_args()

    if args.func is not None:
        code: int = args.func(args)
        if not code:
            return
        else:
            stderr[0] << f"Botele exited with code {code}."
            return
    else:
        parser.print_help()