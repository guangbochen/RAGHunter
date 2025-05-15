import logging
import os
from typing import Required

from raghunter.backend import DoclingConverter
from raghunter.utils.s3_config import S3Config

logger = logging.getLogger(__name__)


def setup_convert_cmd(subparsers):
    convert_parser = subparsers.add_parser("convert", help="Converting input document to supported RAG doc format")
    convert_parser.add_argument(
        "--source", type=str, help="Specify the local source directory or s3 bucket path to process", required=True
    )
    convert_parser.add_argument(
        "--output", type=str, help="Specify the output directory", default="output"
    )
    convert_parser.add_argument(
        "--backend", type=str, help="Specify the converter backend", default="docling", choices=["docling"]
    )
    convert_parser.add_argument(
        "--worker", type=int, help="Number of workers", default=3
    )
    convert_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    convert_parser.add_argument("--use-s3", action="store_true", help="Enable S3 support for input")
    convert_parser.add_argument("--save-to-s3", action="store_true", help="Save output to S3")
    convert_parser.set_defaults(func=handle)


def handle(args):
    print(f"Converting RAGHunter with input: {args.source}, output dir: {args.output}, backend: {args.backend}")
    if args.debug:
        print("Debug mode enabled")

    if args.backend == "docling":
        converter = DoclingConverter()
    else:
        raise ValueError(f"Unsupported backend: {args.backend}")

    if args.use_s3:
        s3_config = S3Config()
        is_valid, error_msg = s3_config.validate()
        if not is_valid:
            logger.error(f"S3 configuration error: {error_msg}")
            return
    
    source = args.source
    ## process input from s3
    if args.use_s3:
        print("Processing S3 input")
        s3 = S3Config()
        s3.sync_to_local(prefix=source, local_dir='data')
        source = 'data' # use local dir as source if s3 is used

    if os.path.isdir(source):
        print("Processing directory:")
        for file in os.listdir(source):
            file_path = os.path.join(source, file)
            if os.path.isfile(file_path):
                print(f"Converting file: {file}")
                converter.convert_and_save(file_path, args.output)
    else:
        # raise error if input is not a directory
        raise ValueError(f"Input {args.source} is not a directory")