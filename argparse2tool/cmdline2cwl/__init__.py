import logging
import re
import sys
from argparse2tool import load_argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Arg2CWLParser:
    def __init__(self):
        ap = load_argparse()  # avoid circular imports
        help_text = """
        argparse2tool forms CWL command line tools from Python tools
        Example: $ python program.py --generate_cwl_tool -b python
        """
        arg2cwl_parser = ap.ArgumentParser(prog=sys.argv[0], description=help_text,
                                           formatter_class=ap.RawDescriptionHelpFormatter, add_help=False)
        arg2cwl_parser.add_argument('tools', nargs='*',
                                    help='Command for running your tool(s), without arguments')
        arg2cwl_parser.add_argument('-d', '--directory',
                                    help='Directory to store CWL tool descriptions')
        arg2cwl_parser.add_argument('-b', '--basecommand',
                                    help='Command that appears in `basecommand` field in CWL tool '
                                         'instead of the default one')
        arg2cwl_parser.add_argument('-o', '--output_section', metavar='FILENAME',
                                    help='File with output section which will be put to a formed CWL tool')
        arg2cwl_parser.add_argument('-go', '--generate_outputs', action='store_true',
                                    help='Form output section from args than contain `output` keyword in their names')
        arg2cwl_parser.add_argument('--help_arg2cwl',
                                    help='Show this help message and exit', action='help')
        self.parser = arg2cwl_parser

    def process_arguments(self):
        self.parser.add_argument('--generate_cwl_tool', action='store_true')
        self.args = self.parser.parse_args()
        logger.debug('sys argv: ', sys.argv)
        commands = [self.parser.prog.split('/')[-1]]
        if self.args.tools:
            commands.extend(self.args.tools)
        command = ' '.join(commands)
        kwargs = dict()
        kwargs['command'] = command.strip()

        shebang = re.search(r'\./[\w-]*?.py$', self.parser.prog)
        if shebang:
            kwargs['basecommand'] = shebang.group(0)

        formcommand = ''
        if kwargs.get('basecommand', ''):
            formcommand += kwargs['basecommand']
        else:
            formcommand += kwargs['command']

        attrs = ['directory', 'output_section', 'basecommand', 'generate_outputs']
        for arg in attrs:
            if getattr(self.args, arg):
                kwargs[arg] = getattr(self.args, arg)

        if kwargs.get('output_section', ''):
            formcommand += ' -o FILENAME'
        if kwargs.get('basecommand', ''):
            formcommand += ' -b {0}'.format(kwargs['basecommand'])
        if kwargs.get('generate_outputs', ''):
            formcommand += ' -go'
        kwargs['formcommand'] = formcommand
        return kwargs
