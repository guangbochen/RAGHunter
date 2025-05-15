"""Main entry point for RAGHunter."""
import argparse
import signal
import sys

from raghunter.cmd import setup_convert_cmd
from raghunter.cmd.version import setup_version_cmd

def handle_signal(sig, frame):
    """Handle interrupt signals."""
    sys.exit(0)


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RAGHunter",
        conflict_handler="resolve",
        add_help=True
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    setup_convert_cmd(subparsers)
    setup_version_cmd(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()