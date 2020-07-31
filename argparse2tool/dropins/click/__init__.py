import os
import re
import sys

from click import click_cwl_translation as cct
from argparse2tool.cmdline2cwl import cwl_tool as cwlt
from argparse2tool import load_click
from argparse2tool.cmdline2cwl import Arg2CWLParser

click = load_click()
__selfmodule__ = sys.modules[__name__]
# This fetches a reference to ourselves

__click_exports__ = list(filter(lambda x: not x.startswith('__'), dir(click)))
# Set the attribute on ourselves.
for x in __click_exports__:
    setattr(__selfmodule__, x, getattr(click, x))


class Arg2CWLMixin:
    def __call__(self, *args, **kwargs):
        arg2cwl_parser = Arg2CWLParser()
        if '--generate_cwl_tool' in sys.argv:

            arg2cwl_options = arg2cwl_parser.process_arguments()
            if hasattr(self, 'commands'):
                for command in self.commands.values():
                    self.form_tool(arg2cwl_options, command)
            else:
                self.form_tool(arg2cwl_options)
            sys.exit()

        elif '--help_arg2cwl' in sys.argv:
            arg2cwl_parser.parser.print_help()
            sys.exit()
        else:
            click.BaseCommand.__call__(self, *args, **kwargs)

    def form_tool(self, arg2cwl_options, command=None):
        name = os.path.basename(sys.argv[0])
        if command is None:
            command = self
        else:
            name += ' %s' % command.name

        tool = cwlt.CWLTool(name,
                            command.help,
                            arg2cwl_options['formcommand'],
                            arg2cwl_options.get('basecommand', ''),
                            arg2cwl_options.get('output_section', ''))

        ct = cct.ClickCWLTranslation()
        for option in command.params:
            cwl_param = ct.get_cwl_param(option)
            if cwl_param is not None:
                tool.inputs.append(cwl_param)
                if isinstance(cwl_param, cwlt.OutputParam):
                    tool.outputs.append(cwl_param)
        data = tool.export()
        self._write_tool(tool, data, arg2cwl_options.get('directory', ''))

    def _write_tool(self, tool, data, directory):
        filename = '{0}.cwl'.format(tool.name.replace('.py', ''))
        filename = re.sub(r'\s+', '-', filename)
        if directory and directory[-1] != '/':
            directory += '/'
        filename = directory + filename
        with open(filename, 'w') as f:
            f.write(data)
        print(data)


class Arg2CWLCommand(Arg2CWLMixin, click.Command):
    pass


class Arg2CWLGroup(Arg2CWLMixin, click.Group):
    pass


def command(name=None, cls=Arg2CWLCommand, **attrs):
    """override click function 'command' """

    return click.command(name, cls, **attrs)


def group(name=None, **attrs):
    """override click function 'group' """

    attrs.setdefault('cls', Arg2CWLGroup)
    return command(name, **attrs)
