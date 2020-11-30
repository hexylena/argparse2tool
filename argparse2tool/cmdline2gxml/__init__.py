import logging
import sys
from argparse2tool import load_argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Arg2GxmlParser:
    def __init__(self):
        ap = load_argparse()  # avoid circular imports
        help_text = (
            "argparse2tool forms Galaxy XML and CWL tools from Python scripts.\n"
            "You are currently using the Galaxy XML invocation which may have different options from the CWL invocation."
        )
        arg2tool_parser = ap.ArgumentParser(
            prog=sys.argv[0], description=help_text,
            formatter_class=ap.RawDescriptionHelpFormatter, add_help=False
        )

        arg2tool_parser.add_argument('--help', help='Show this help message and exit', action='help')
        self.parser = arg2tool_parser

    def process_arguments(self):
        self.parser.add_argument('--generate_galaxy_xml', action='store_true')
        self.parser.add_argument('--command', action='store', default="")
        return vars(self.parser.parse_args())
