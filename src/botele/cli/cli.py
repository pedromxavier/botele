""" botele: A Python Telegram Bot Factory
"""
import argparse
from pathlib import Path

from .run import run
from .kill import kill
from .make import make
from .list_ import list_
from .alive import alive
from .setup import setup
from .install import install

from .banner import BOTELE_BANNER

from cstream import Stream, stderr, stdwar, stdlog, stdout

stdbot = Stream(fg="BLUE", sty="DIM")

class BotArgumentParser(argparse.ArgumentParser):

    def print_help(self, from_help: bool=True):
        if from_help: stdbot[0] << BOTELE_BANNER
        argparse.ArgumentParser.print_help(self, stdout[0])

    def error(self, message):
        stderr[0] << f"Error: {message}"
        self.print_help(from_help=False)
        exit(1)

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
    parser.add_argument("--debug", action="store_true", help="Enter debug mode")
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers()

    ## RUN
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "bot", type=str, nargs="*", action="store", help="Bot identifier"
    )
    run_parser.add_argument(
        "--all", dest="all", action="store_true", help="Run all installed bots"
    )
    run_parser.set_defaults(func=run)

    ## LIST
    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_)

    ## ALIVE
    alive_parser = subparsers.add_parser("alive")
    alive_parser.set_defaults(func=alive)

    ## RUN
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "bot", type=str, nargs="*", action="store", help="Bot identifiers."
    )
    run_parser.add_argument(
        "--all", action="store_true", help="Run all installed bots."
    )
    run_parser.add_argument(
        "--wait", action="store_true", help="Wait for bot execution. Press CTRL+C to interrupt all started bots."
    )
    run_parser.set_defaults(func=run)

    ## KILL
    kill_parser = subparsers.add_parser("kill")
    kill_parser.add_argument(
        "bot", type=str, nargs="*", action="store", help="Bot identifiers."
    )
    kill_parser.add_argument(
        "--all", action="store_true"
    )
    kill_parser.set_defaults(func=kill)

    ## SETUP
    setup_parser = subparsers.add_parser("setup")
    setup_parser.add_argument(
        "path", type=str, action="store", default=Path.cwd(), help="Bot folder path"
    )
    setup_parser.add_argument(
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