import logging
import re
import sys
from builtins import range

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = '0.3.1'


def load_argparse():
    ARGPARSE_NUMBER = 1
    return load_conflicting_package('argparse', 'gxargparse', ARGPARSE_NUMBER)


def load_conflicting_package(name, not_name, module_number):
    """Load a conflicting package
    Some assumptions are made, namely that your package includes the "official"
    one as part of the name. E.g. gxargparse/argparse, you would call this with:

        >>> real_argparse = load_conflicting_package('argparse', 'gxargparse', 1)

     http://stackoverflow.com/a/6032023
    """
    import imp
    for i in range(0, 100):
        random_name = 'random_name_%d' % (i,)
        if random_name not in sys.modules:
            break
        else:
            random_name = None
    if random_name is None:
        raise RuntimeError("Couldn't manufacture an unused module name.")
    # NB: This code is unlikely to work for nonstdlib overrides.
    # This will hold the correct sys.path for the REAL argparse
    for path in sys.path:
        try:
            (f, pathname, desc) = imp.find_module(name, [path])
            if not_name not in pathname and desc[2] == module_number:
                module = imp.load_module(random_name, f, pathname, desc)
                # f.close()
                return sys.modules[random_name]
        except:
            # Many sys.paths won't contain the module of interest
            pass
    return None


class Arg2CWLParser:
    def __init__(self):
        ap = load_argparse()  # avoid circular imports
        help_text = """
        argparse2cwl forms CWL command line tool from Python tool
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
