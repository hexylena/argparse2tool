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


class ArgumentParser(ap.ArgumentParser):

    # argument_list = []

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
        if '--generate_cwl_tool' in sys.argv:
            # assuming all passed arguments are either commands or argparse2cwl flags
            command = ''
            shebang = re.search(r'\./\w*?.py$', sys.argv[0])
            for arg in sys.argv:
                if not arg.startswith('--'):
                    command += '{0} '.format(arg.split('/')[-1])
                else:
                    command = command.strip()
                    kwargs['command'] = command
                    break
            if '-f' in sys.argv:
                kwargs['path'] = sys.argv[sys.argv.index('-f')+1]
            if '--basecommand' in sys.argv:
                kwargs['basecommand'] = sys.argv[sys.argv.index('--basecommand')+1]
            elif shebang:
                kwargs['basecommand'] = shebang.group(0)
            self.parse_args_cwl(*args, **kwargs)
        # TODO: reorganize to a separate CLI
        elif '--generate_galaxy_xml' in sys.argv:
            self.parse_args_galaxy_nouse(*args, **kwargs)
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
                    tool = cwlt.CWLTool(argp.prog, argp.description, kwargs.get('basecommand', ''))
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
