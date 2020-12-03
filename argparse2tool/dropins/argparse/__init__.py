import re
import sys
from argparse2tool import load_argparse
from argparse2tool.cmdline2gxml import Arg2GxmlParser
from argparse2tool.cmdline2cwl import Arg2CWLParser

import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
from . import argparse_galaxy_translation as agt
from . import argparse_cwl_translation as act
from argparse2tool.cmdline2cwl import cwl_tool as cwlt

ap = load_argparse()

# This fetches a reference to ourselves
__selfmodule__ = sys.modules[__name__]
# Static list of imports
__argparse_exports__ = list(filter(lambda x: not x.startswith('__'), dir(ap)))
# Set the attribute on ourselves.
for x in __argparse_exports__:
    setattr(__selfmodule__, x, getattr(ap, x))

tools = []


class ArgumentParser(ap.ArgumentParser):

    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=ap.ArgumentDefaultsHelpFormatter,
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
        arg2gxml_parser = Arg2GxmlParser()
        arg2cwl_parser = Arg2CWLParser()

        if '--generate_galaxy_xml' in sys.argv:
            kwargs = arg2gxml_parser.process_arguments()
            self.parse_args_galaxy(*args, **kwargs)
        elif '--generate_cwl_tool' in sys.argv:
            kwargs = arg2cwl_parser.process_arguments()
            self.parse_args_cwl(*args, **kwargs)
        else:
            return ap.ArgumentParser.parse_args(self, *args, **kwargs)

    def parse_args_cwl(self, *args, **kwargs):
        for argp in tools:
            # make subparser description out of its help message
            if argp._subparsers:
                # there were cases during testing, when instances other than _SubParsesAction type
                # got into ._subparsers._group_actions
                for subparser in filter(lambda action: isinstance(action, ap._SubParsersAction),
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
                                        kwargs.get('output_section', ''))
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
                    filename = '{0}.cwl'.format(tool.name.replace('.py', ''))
                    filename = re.sub(r'\s+', '-', filename)
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

    def parse_args_galaxy(self, *args, **kwargs):
        for argp in tools:
            # make subparser description out of its help message
            if argp._subparsers:
                # there were cases during testing, when instances other than _SubParsesAction type
                # got into ._subparsers._group_actions
                for subparser in filter(lambda action: isinstance(action, ap._SubParsersAction),
                                        argp._subparsers._group_actions):
                    for choice_action in subparser._choices_actions:
                        subparser.choices[choice_action.dest].description = choice_action.help
            else:
                if kwargs.get('command', argp.prog) in argp.prog:
                    data = self._parse_args_galaxy_argp(argp)
                    print(data)
                else:
                    continue
        sys.exit(0)

    def _parse_args_galaxy_argp(self, argp):
        try:
            version = self.print_version() or '1.0'
        except AttributeError:  # handle the potential absence of print_version
            version = '1.0'
        tool = gxt.Tool(argp.prog,
                        argp.prog.replace(" ", "_"),
                        version,
                        argp.description,
                        "python "+argp.prog,
                        interpreter=None,
                        version_command='python %s --version' % argp.prog)

        inputs = gxtp.Inputs()
        outputs = gxtp.Outputs()

        at = agt.ArgparseGalaxyTranslation()
        # Only build up arguments if the user actually requests it
        for result in argp.argument_list:
            # I am SO thankful they return the argument here. SO useful.
            argument_type = result.__class__.__name__
            # http://stackoverflow.com/a/3071
            if hasattr(at, argument_type):
                methodToCall = getattr(at, argument_type)
                gxt_parameter = methodToCall(result, tool=tool)
                if gxt_parameter is not None:
                    if isinstance(gxt_parameter, gxtp.InputParameter):
                        inputs.append(gxt_parameter)
                    else:
                        outputs.append(gxt_parameter)

        # TODO: replace with argparse-esque library to do this.
        stdout = gxtp.OutputData('default', 'txt')
        stdout.command_line_override = '> $default'
        outputs.append(stdout)

        tool.inputs = inputs
        tool.outputs = outputs
        if argp.epilog is not None:
            tool.help = argp.epilog
        else:
            tool.help = "TODO: Write help"

        return tool.export()
