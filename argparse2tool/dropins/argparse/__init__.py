import os.path
import re
import shutil
import sys
from argparse2tool import (
    load_argparse,
    remove_extension
)
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
# set of prog names where the argparser actually should be represented
# as a macro, i.e. XYZ will be in the set if there is a
# ArgumentParser(..., parents=[XYZ], ...)
macros = set()

# mapping tools to list of required macros (which are actually identical to the
# parents parameter passed ArgumentParser. but I could not find out how this is
# stored in the created ArgumentParser objects
used_macros = dict()


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
        global macros
        global used_macros

        self.argument_list = []
        self.argument_names = []
        tools.append(self)
        if len(parents) > 0:
            p = set([remove_extension(_.prog) for _ in parents])
            macros = macros.union(p)
            used_macros[remove_extension(prog)] = p
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
                        else:
                            print("%s not implemented (%s)" % (argument_type, result.option_strings), file=sys.stderr)

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
        global used_macros

        directory = kwargs.get('directory', None)
        macro = kwargs.get('macro', None)

        # copy macros to destination dir
        if directory and macro:
            for i, m in enumerate(macro):
                macro[i] = os.path.basename(m)
                shutil.copyfile(m, os.path.join(directory, macro[i]))

        # since macros can also make use of macros (i.e. the parent relation
        # specified in the arguments can be nester) we need to extend the
        # used macros such that really all are included
        ext_used_macros = dict()
        for tool, macros in used_macros.items():
            ext_used_macros[tool] = set()
            q = list(macros)
            while len(q) > 0:
                m = q.pop()
                if m in used_macros:
                    q.extend(used_macros[m])
                ext_used_macros[tool].add(m)
        used_macros = ext_used_macros

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
                    data = self._parse_args_galaxy_argp(argp, macro)
                    if directory:
                        if directory[-1] != '/':
                            directory += '/'
                        filename = remove_extension(argp.prog) + ".xml"
                        filename = directory + filename
                        with open(filename, 'w') as f:
                            f.write(data)
                    else:
                        print(data)
                else:
                    continue
        sys.exit(0)

    def _parse_args_galaxy_argp(self, argp, macro):
        global macros
        global used_macros

        try:
            version = self.print_version() or '1.0'
        except AttributeError:  # handle the potential absence of print_version
            version = '1.0'

        prog = remove_extension(argp.prog)

        # tid = argp.prog.split()[-1]

        # get the list of file names of the used macros
        mx = used_macros.get(prog, [])
        mx = sorted(["%s.xml" % _.split(" ")[-1] for _ in mx])

        if prog not in macros:
            tpe = gxt.Tool
            if macro:
                mx.extend(macro)
        else:
            tpe = gxt.MacrosTool

        tool = tpe(prog,
                   prog.replace(" ", "_"),
                   version,
                   argp.description,
                   "python "+argp.prog,
                   interpreter=None,
                   version_command='python %s --version' % argp.prog,
                   macros=mx)

        inputs = tool.inputs
        outputs = tool.outputs
        sections = dict()

        at = agt.ArgparseGalaxyTranslation()

        for group in argp._action_groups:
            if group in [argp._positionals, argp._optionals]:
                continue
            argument_type = group.__class__.__name__
            methodToCall = getattr(at, argument_type)
            sections[group] = methodToCall(group, tool=tool)

        for action in argp._actions:
            # I am SO thankful they return the argument here. SO useful.
            argument_type = action.__class__.__name__
            # http://stackoverflow.com/a/3071
            if hasattr(at, argument_type):
                methodToCall = getattr(at, argument_type)
                gxt_parameter = methodToCall(action, tool=tool)
                if gxt_parameter is None:  # e.g. for help and version actions
                    continue
                if not isinstance(gxt_parameter, gxtp.InputParameter):
                    outputs.append(gxt_parameter)
                elif action.container in sections:
                    sections[action.container].append(gxt_parameter)
                else:
                    inputs.append(gxt_parameter)
            else:
                print("%s not implemented (%s)" % (argument_type, result.option_strings), file=sys.stderr)

        for section in sections:
            inputs.append(sections[section])


#         print("argp._action_groups %s" % argp._action_groups)
#         # Only build up arguments if the user actually requests it
#         for result in argp.argument_list:
#             # I am SO thankful they return the argument here. SO useful.
#             argument_type = result.__class__.__name__
#             print("_parse_args_galaxy_argp %s type %s [%s]" % (getattr(result, "title", "no title"), argument_type, hasattr(at, argument_type)))
#             # http://stackoverflow.com/a/3071
#             if hasattr(at, argument_type):
#                 methodToCall = getattr(at, argument_type)
#                 gxt_parameter = methodToCall(result, tool=tool)
#                 if gxt_parameter is not None:
#                     if isinstance(gxt_parameter, gxtp.InputParameter):
#                         inputs.append(gxt_parameter)
#                     else:
#                         outputs.append(gxt_parameter)

        if prog in used_macros:
            for m in sorted(used_macros[prog]):
                inputs.append(gxtp.ExpandIO(m + "_inmacro"))
                outputs.append(gxtp.ExpandIO(m + "_outmacro"))

        if prog not in macros:
            # TODO: replace with argparse-esque library to do this.
            stdout = gxtp.OutputData('default', 'txt')
            stdout.command_line_override = '> $default'
            outputs.append(stdout)

        if argp.epilog is not None:
            tool.help = argp.epilog
        else:
            tool.help = "TODO: Write help"
        return tool.export()
