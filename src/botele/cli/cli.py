import argparse

from .run import run
from .make import make
from .list import list_
from .setup import setup
from .install import install

from cstream import Stream, stderr, stdwar, stdlog, stdout


def main():
    """"""

    params = {"description": __doc__}

    parser = argparse.ArgumentParser(**params)
    parser.add_argument(
        "-v",
        "--verbose",
        choices=range(4),
        type=int,
        action="store",
        default=0,
        help="Output verbosity.",
    )
    parser.add_argument("--debug", action="store_true", help="Enter debug mode.")
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("bot", type=str, action="store", help="Bot identifier")
    run_parser.set_defaults(func=run)

    setup_parser = subparsers.add_parser("setup")
    setup_parser.add_argument(
        "path", type=str, nargs="?", action="store", help="Bot folder path"
    )
    setup_parser.add_argument(
        "-n",
        "--name",
        dest="name",
        action="store",
        help="Bot identifier (defaults to directory name)",
    )
    setup_parser.set_defaults(func=setup)

    make_parser = subparsers.add_parser("make")
    make_parser.add_argument(
        "path", type=str, nargs="?", action="store", help="Bot folder path"
    )
    make_parser.set_defaults(func=make)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument(
        "path", type=str, nargs="?", action="store", help="Bot folder path"
    )
    install_parser.set_defaults(func=install)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_)

    args = parser.parse_args()

    if args.debug:
        Stream.set_lvl(4)
        stdwar[0] << "Debug mode enabled."
    else:
        Stream.set_lvl(args.verbose)

    if args.func is not None:

        stdlog[4] << f"CLI ARGS:\n\t{args}"

        code: int = args.func(args)

        if not code:
            stdlog[1] << f"Botele exited with code {code}."
            return
        else:
            stderr[1] << f"Botele exited with code {code}."
            return
    else:
        parser.print_help(stdout)