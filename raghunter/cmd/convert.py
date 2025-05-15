import logging

logger = logging.getLogger(__name__)


def setup_convert_cmd(subparsers):
    start_parser = subparsers.add_parser("convert", help="Convert input document to Markdown or JSON format")
    start_parser.add_argument(
        "--input", type=str, help="Specify the input directory", required=True
    )
    start_parser.add_argument(
        "--output", type=str, help="Specify the output directory", default="output"
    )
    start_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    start_parser.set_defaults(func=handle)


def handle(args):
    print(f"Starting RAGHunter with input: {args.input}, output: {args.output}")
    if args.debug:
        print("Debug mode enabled")
