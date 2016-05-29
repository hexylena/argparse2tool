from builtins import object
import os

from jinja2 import Environment, FileSystemLoader


class Param(object):
    def __init__(self, id, position=None, description=None, default=None, prefix=None, optional=False):
        self.id = id
        self.position = position
        self.default = default
        self.prefix = prefix
        self.optional = optional
        if description:
            self.description = description.replace(':', ' -')  # `:` is a special character and must be replaced with smth
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

    def __init__(self, name, description, basecommand=None):
        self.name = name
        if description:
            self.description = description.replace('\n', '\n  ')
        else:
            self.description = None
        env = Environment(
            loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))),
            trim_blocks=True,
            lstrip_blocks=True)
        self.template = env.get_template('cwltool_inputs.j2')
        if basecommand:
            self.basecommands = [basecommand]
        else:
            self.basecommands = self.name.split()
        self.inputs = []
        self.outputs = []

    def export(self):
        return self.template.render(tool=self,
                                    basecommand=self.basecommands)
