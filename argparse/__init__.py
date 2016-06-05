from __future__ import print_function
from __future__ import absolute_import
from builtins import range
import sys

import re

from argparse.cwl_tool import CWLTool


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
__argparse_exports__ = ['HelpFormatter', 'RawDescriptionHelpFormatter',
                        'ArgumentDefaultsHelpFormatter', 'FileType',
                        'SUPPRESS', 'OPTIONAL', 'ZERO_OR_MORE', 'ONE_OR_MORE',
                        'PARSER', 'REMAINDER', '_UNRECOGNIZED_ARGS_ATTR',
                        '_VersionAction']

# Set the attribute on ourselves.
for x in __argparse_exports__:
    setattr(__selfmodule__, x, getattr(ap, x))

tools = []


def get_arg2cwl_parser():
    help_text = """
    argparse2cwl forms CWL command line tool from Python tool
    """
    arg2cwl_parser = ap.ArgumentParser(prog=sys.argv[0], description=help_text, add_help=False)
    arg2cwl_parser.add_argument('tools', nargs='*',
                                help='Command for running your tool(s), without arguments')
    arg2cwl_parser.add_argument('-d', '--directory',
                                help='Directory for placing formed CWL tool')
    arg2cwl_parser.add_argument('-b', '--basecommand',
                                help='Command that appears in `basecommand` field in CWL tool')
    arg2cwl_parser.add_argument('-o', '--output_section',
                                help='File with output section which will be appended to a formed CWL tool')
    arg2cwl_parser.add_argument('-ha', '--help_arg2cwl',
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
        self.argument_list.append(result)

    def parse_args(self, *args, **kwargs):

        arg2cwl_parser = get_arg2cwl_parser()

        if '--generate_cwl_tool' in sys.argv:
            arg2cwl_parser.add_argument('--generate_cwl_tool', action='store_true')
            arg2cwl_args = arg2cwl_parser.parse_args(*args, **kwargs)

            commands = [arg2cwl_parser.prog.split('/')[-1]]
            if arg2cwl_args.tools:
                commands.extend(arg2cwl_args.tools)
            command = ' '.join(commands)
            kwargs['command'] = command.strip()

            attrs = ['directory', 'output_section', 'basecommand']
            for arg in attrs:
                if getattr(arg2cwl_args, arg):
                    kwargs[arg] = getattr(arg2cwl_args, arg)

            shebang = re.search(r'\./\w*?.py$', arg2cwl_parser.prog)
            if shebang:
                kwargs['basecommand'] = shebang.group(0)

            self.parse_args_cwl(*args, **kwargs)

        elif '--generate_galaxy_xml' in sys.argv:
            self.parse_args_galaxy_nouse(*args, **kwargs)

        elif '--help_arg2cwl' in sys.argv:
            arg2cwl_parser.print_help()
            sys.exit()
        # TODO: discuss standalone CLI, i.e. $ argparse2cwl <tool command> <options>
        else:
            return ap.ArgumentParser.parse_args(self, *args, **kwargs)

    def parse_args_cwl(self, *args, **kwargs):
        for argp in tools:
            # make subparser description out of its help message
            if argp._subparsers:
                for subparser in argp._subparsers._group_actions:
                    for choice_action in subparser._choices_actions:
                        subparser.choices[choice_action.dest].description = choice_action.help
            # if the command is subparser, we don't need its CWL wrapper
            else:
                # build up wrappers if the user actually requests it, otherwise build all wrappers
                if kwargs.get('command', argp.prog) in argp.prog:
                    tool = cwlt.CWLTool(argp.prog,
                                        argp.description,
                                        kwargs.get('basecommand', ''),
                                        kwargs.get('output_section', ''))
                    at = act.ArgparseCWLTranslation()
                    for result in argp._actions:
                        argument_type = result.__class__.__name__
                        # http://stackoverflow.com/a/3071
                        if hasattr(at, argument_type):
                            methodToCall = getattr(at, argument_type)
                            cwlt_parameter = methodToCall(result)
                            if cwlt_parameter is not None:
                                tool.inputs.append(cwlt_parameter)
                                if isinstance(cwlt_parameter, cwlt.OutputParam):
                                    tool.outputs.append(cwlt_parameter)

                    if argp.epilog is not None:
                        tool.help = argp.epilog
                    else:
                        tool.help = "TODO: Write help"

                    data = tool.export()
                    filename = '{0}.cwl'.format(tool.name.replace('.py',''))
                    filename = re.sub('\s+', '-', filename)
                    with open(kwargs.get('path', '') + filename, 'w') as f:
                        f.write(data)
                    print(data)
                else:
                    continue
        sys.exit()

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
