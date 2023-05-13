#!/usr/bin/env python3
"""Convert a Python script to single line.

Usage:

  echo 'print("Hello")' | python3 pyline.py 2>/dev/null

Test:

  echo 'print("Hello")' | python3 pyline.py | python3

"""
import argparse
import base64
import logging
import sys

try:
    import colorama

    colorama.init(autoreset=True)
    COLORAMA_ENABLED = True
except ImportError:
    COLORAMA_ENABLED = False


handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s %(message)s")

l_debug = "[*]"
l_info = "[+]"
l_warning = "[-]"
l_error = "[!]"
l_critical = "[!!!]"

if COLORAMA_ENABLED:
    l_debug = colorama.Fore.CYAN + l_debug
    l_info = colorama.Fore.GREEN + l_info
    l_warning = colorama.Fore.YELLOW + l_warning
    l_error = colorama.Fore.RED + l_error
    l_critical = colorama.Fore.RED + l_critical

logging.addLevelName(logging.DEBUG, l_debug)
logging.addLevelName(logging.INFO, l_info)
logging.addLevelName(logging.WARNING, l_warning)
logging.addLevelName(logging.ERROR, l_error)
logging.addLevelName(logging.CRITICAL, l_critical)

handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[handler])

__version__ = "1.0.0"


def exec_base64(source, import_base64=True):
    encoded = base64.b64encode(bytes(source, encoding="utf-8")).decode()
    string = 'exec(base64.b64decode("{}"))\n'.format(encoded)
    if import_base64:
        string = "import base64;" + string
    return string


def _handle(args):
    if args.version:
        print(__version__)
        return 0
    source = args.input.read()
    out = exec_base64(source)
    args.output.write(out)
    logging.info(
        f"single line payload generated from {args.input.name} to {args.output.name}"
    )
    return 0


def _cli():
    parser = argparse.ArgumentParser(
        prog="pyline",
        description="%(prog)s CLI tool to generate single line payload.",
    )

    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "--raise-exceptions",
        action="store_true",
        help="Raise exceptions instead of just printing them.",
    )

    parser.add_argument(
        "input",
        nargs="?",  # required to be able to pipe to stdin
        help="input file",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )

    args = parser.parse_args()

    try:
        return _handle(args)
    except Exception as e:
        logging.error(str(e))
        if args.raise_exceptions:
            raise
        logging.debug("use `--raise-exceptions` to see full trace back.")
        return 1


if __name__ == "__main__":
    sys.exit(_cli())  # pragma: no cover
