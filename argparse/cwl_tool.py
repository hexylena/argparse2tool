from builtins import object
import os

from jinja2 import Environment, FileSystemLoader


class Param(object):
    def __init__(self, id, position=None, description=None, default=None, prefix=None, optional=False, items_type=None):
        self.id = id
        self.position = position
        self.default = default
        self.prefix = prefix
        self.optional = optional
        self.items_type = items_type
        if description:
            self.description = description.replace(':', ' -') \
                .replace('\n', ' ')  # `:` is a special character and must be replaced with smth
        else:
            self.description = None


class OutputParam(Param):
    type = "File"


class InputParam(Param):
    pass


class TextParam(InputParam):
    type = 'string'


class _NumericParam(InputParam):
    pass


class IntegerParam(_NumericParam):
    type = 'int'


class FloatParam(_NumericParam):
    type = 'float'


class BooleanParam(InputParam):
    type = 'boolean'


class ArrayParam(InputParam):
    type = 'array'


class ChoiceParam(InputParam):
    type = 'enum'

    def __init__(self, **kwargs):
        self.choices = list(kwargs.pop('choices', []))
        super(ChoiceParam, self).__init__(**kwargs)


class DataParam(InputParam):
    type = 'File'


class CWLTool(object):

    def __init__(self, name, description, basecommand=None, output_file=None):
        self.name = name
        self.output_file = output_file
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
                                    basecommand=self.basecommands,
                                    inputs=inputs,
                                    outputs=outputs)
