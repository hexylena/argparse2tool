import re
import os

from jinja2 import Environment, FileSystemLoader
from argparse2tool import __version__


class Param:
    def __init__(self, id, type, position=None, description=None, default=None, prefix=None, optional=False, items_type=None, **kwargs):
        self.id = id
        self.position = position
        self.type = type
        self.default = default
        self.prefix = prefix
        self.optional = optional
        self.items_type = items_type
        if description:
            self.description = description.replace(':', ' -') \
                .replace('\n', ' ')  # `:` is a special character and must be replaced with smth
            self.description = re.sub(r'\s{2,}', ' ', self.description)
        else:
            self.description = None
        if self.type == 'enum':
            self.choices = list(kwargs.pop('choices', []))


class OutputParam(Param):
    pass


class CWLTool(object):

    def __init__(self, name, description, formcommand, basecommand=None, output_file=None):
        self.name = name
        self.output_file = output_file  # file with manually filled output section
        if description:
            self.description = description.replace('\n', '\n  ')
        else:
            self.description = None
        self.env = Environment(
            loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))),
            trim_blocks=True,
            lstrip_blocks=True)
        if basecommand:
            self.basecommands = [basecommand]
        else:
            self.basecommands = self.name.split()
        self.formcommand = formcommand
        self.inputs = []
        self.outputs = []

    def export(self):
        inputs_template = self.env.get_template('cwltool_inputs.j2')
        outputs_template = self.env.get_template('cwltool_outputs.j2')
        main_template = self.env.get_template('cwltool.j2')
        inputs = inputs_template.render(tool=self, basecommand=self.basecommands)
        if self.output_file:
            with open(self.output_file) as f:
                outputs = f.read()
        else:
            outputs = outputs_template.render(tool=self)
        return main_template.render(tool=self,
                                    version=__version__,
                                    formcommand=self.formcommand,
                                    stripped_options_command=re.sub('-.*', '', self.formcommand),
                                    basecommand=self.basecommands,
                                    inputs=inputs,
                                    outputs=outputs)
