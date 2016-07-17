from __future__ import print_function
from __future__ import absolute_import
from builtins import range
import sys
import logging

import re

from argparse.cwl_tool import CWLTool

__version__ = '0.2.7'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_conflicting_package(name, not_name, local_module):
    """Load a conflicting package
    Some assumptions are made, namely that your package includes the "official"
    one as part of the name. E.g. gxargparse/argparse, you would call this with:

        >>> real_argparse = load_conflicting_package('argpargase', 'gxargparse',
        ...                                          sys.modules[load_conflicting_package.__module__])

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
            if not_name not in pathname and desc[2] == 1:
                module = imp.load_module(random_name, f, pathname, desc)
                f.close()
                return sys.modules[random_name]
        except:
            # Many sys.paths won't contain the module of interest
            pass
    return None

ap = load_conflicting_package('argparse', 'gxargparse', sys.modules[load_conflicting_package.__module__])
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
from . import argparse_galaxy_translation as agt
from . import argparse_cwl_translation as act
from . import cwl_tool as cwlt

# This fetches a reference to ourselves
__selfmodule__ = sys.modules[load_conflicting_package.__module__]
# Static list of imports
__argparse_exports__ = list(filter(lambda x: not x.startswith('__'), dir(ap)))
# Set the attribute on ourselves.
for x in __argparse_exports__:
    setattr(__selfmodule__, x, getattr(ap, x))

tools = []


def get_arg2cwl_parser():
    help_text = """
    argparse2cwl forms CWL command line tool from Python tool
    Example: $ python program.py --generate_cwl_tool -b python
    """
    arg2cwl_parser = ap.ArgumentParser(prog=sys.argv[0], description=help_text,
                                       formatter_class=RawDescriptionHelpFormatter, add_help=False)
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
    arg2cwl_parser.add_argument('--map_ids', action='store_true',
                                help='Map identifier to the corresponding CommandInputParameter')
    arg2cwl_parser.add_argument('--help_arg2cwl',
                                help='Show this help message and exit', action='help')
    return arg2cwl_parser


class ArgumentParser(ap.ArgumentParser):


    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True):

        self.argument_list = []
        self.argument_names = []
        tools.append(self)
        super(ArgumentParser, self).__init__(prog=prog,
                                             usage=usage,
                                             description=description,
                                             epilog=epilog,
                                             parents=parents,
                                             formatter_class=formatter_class,
                                             prefix_chars=prefix_chars,
                                             fromfile_prefix_chars=fromfile_prefix_chars,
                                             argument_default=argument_default,
                                             conflict_handler=conflict_handler,
                                             add_help=add_help)

    def add_argument(self, *args, **kwargs):
        result = ap.ArgumentParser.add_argument(self, *args, **kwargs)
        # to avoid duplicate ids when there's a positional and an optional param with the same dest
        if result.dest in self.argument_names:
            if result.__class__.__name__ == '_AppendConstAction':
                # append_const params with the same dest are populated in job.json
                return
            else:
                result.dest = '_' + result.dest
        self.argument_list.append(result)
        self.argument_names.append(result.dest)

    def parse_args(self, *args, **kwargs):

        arg2cwl_parser = get_arg2cwl_parser()
        if '--generate_cwl_tool' in sys.argv:
            arg2cwl_parser.add_argument('--generate_cwl_tool', action='store_true')
            arg2cwl_args = arg2cwl_parser.parse_args(*args, **kwargs)
            logger.debug('sys argv: ', sys.argv)
            commands = [arg2cwl_parser.prog.split('/')[-1]]
            if arg2cwl_args.tools:
                commands.extend(arg2cwl_args.tools)
            command = ' '.join(commands)
            kwargs['command'] = command.strip()

            shebang = re.search(r'\./[\w-]*?.py$', arg2cwl_parser.prog)
            if shebang:
                kwargs['basecommand'] = shebang.group(0)

            formcommand = ''
            if kwargs.get('basecommand', ''):
                formcommand += kwargs['basecommand']
            else:
                formcommand += kwargs['command']

            attrs = ['directory', 'output_section', 'basecommand', 'generate_outputs', 'map_ids']
            for arg in attrs:
                if getattr(arg2cwl_args, arg):
                    kwargs[arg] = getattr(arg2cwl_args, arg)

            if kwargs.get('output_section', ''):
                formcommand += ' -o FILENAME'
            if kwargs.get('basecommand', ''):
                formcommand += ' -b {0}'.format(kwargs['basecommand'])
            if kwargs.get('generate_outputs', ''):
                formcommand += ' -go'
            if kwargs.get('map_ids', ''):
                formcommand += ' --map_ids'
            kwargs['formcommand'] = formcommand

            self.parse_args_cwl(*args, **kwargs)

        elif '--generate_galaxy_xml' in sys.argv:
            self.parse_args_galaxy_nouse(*args, **kwargs)

        elif '--help_arg2cwl' in sys.argv:
            arg2cwl_parser.print_help()
            sys.exit()
        else:
            return ap.ArgumentParser.parse_args(self, *args, **kwargs)

    def parse_args_cwl(self, *args, **kwargs):
        for argp in tools:
            # make subparser description out of its help message
            if argp._subparsers:
                # there were cases during testing, when instances other than _SubParsesAction type
                # got into ._subparsers._group_actions
                for subparser in filter(lambda action: isinstance(action, _SubParsersAction),
                                        argp._subparsers._group_actions):
                    for choice_action in subparser._choices_actions:
                        subparser.choices[choice_action.dest].description = choice_action.help
            # if the command is subparser itself, we don't need its CWL wrapper
            else:
                # if user provides a generic command like `cnvkit.py` - all possible descriptions are generated
                # if a specific command like `cnvkit.py batch` is given and
                # there are no subparsers - only this description is built
                if kwargs.get('command', argp.prog) in argp.prog:
                    tool = cwlt.CWLTool(argp.prog,
                                        argp.description,
                                        kwargs['formcommand'],
                                        kwargs.get('basecommand', ''),
                                        kwargs.get('output_section', ''),
                                        kwargs.get('map_ids', ''))
                    at = act.ArgparseCWLTranslation(kwargs.get('generate_outputs', False))
                    for result in argp._actions:
                        argument_type = result.__class__.__name__
                        if hasattr(at, argument_type):
                            methodToCall = getattr(at, argument_type)
                            cwlt_parameter = methodToCall(result)
                            if cwlt_parameter is not None:
                                tool.inputs.append(cwlt_parameter)
                                if isinstance(cwlt_parameter, cwlt.OutputParam):
                                    tool.outputs.append(cwlt_parameter)

                    if argp.epilog is not None:
                        tool.description += argp.epilog

                    data = tool.export()
                    filename = '{0}.cwl'.format(tool.name.replace('.py',''))
                    filename = re.sub('\s+', '-', filename)
                    directory = kwargs.get('directory', '')
                    if directory and directory[-1] != '/':
                        directory += '/'
                    filename = directory + filename
                    with open(filename, 'w') as f:
                        f.write(data)
                    print(data)
                else:
                    continue
        sys.exit(0)

    def parse_args_galaxy_nouse(self, *args, **kwargs):
        self.tool = gxt.Tool(
                self.prog,
                self.prog,
                self.print_version() or '1.0',
                self.description,
                self.prog,
                interpreter='python',
                version_command='python %s --version' % sys.argv[0])

        self.inputs = gxtp.Inputs()
        self.outputs = gxtp.Outputs()

        self.at = agt.ArgparseGalaxyTranslation()
        # Only build up arguments if the user actually requests it
        for result in self.argument_list:
            # I am SO thankful they return the argument here. SO useful.
            argument_type = result.__class__.__name__
            # http://stackoverflow.com/a/3071
            if hasattr(self.at, argument_type):
                methodToCall = getattr(self.at, argument_type)
                gxt_parameter = methodToCall(result, tool=self.tool)
                if gxt_parameter is not None:
                    if isinstance(gxt_parameter, gxtp.InputParameter):
                        self.inputs.append(gxt_parameter)
                    else:
                        self.outputs.append(gxt_parameter)

        # TODO: replace with argparse-esque library to do this.
        stdout = gxtp.OutputParameter('default', 'txt')
        stdout.command_line_override = '> $default'
        self.outputs.append(stdout)

        self.tool.inputs = self.inputs
        self.tool.outputs = self.outputs
        if self.epilog is not None:
            self.tool.help = self.epilog
        else:
            self.tool.help = "TODO: Write help"

        data = self.tool.export()
        print(data)
        sys.exit()
