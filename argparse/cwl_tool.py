from builtins import object
import os

from jinja2 import Environment, FileSystemLoader


class Param(object):
    def __init__(self, id, position=None, description=None, default=None):
        self.id = id
        self.position = position
        self.description = description.replace(':', '-')  # `:` is a special character and must be replaced with smth
        self.default = default


class OutputParam(Param):
    type = "File"


class InputParam(Param):
    pass


class TextParam(InputParam):
    type = 'string'
    # def __init__(self, **kwargs):
    #     self.type = 'string'
    #     super(TextParam, self).__init__(**kwargs)


class _NumericParam(InputParam):
    pass
    # def __init__(self, name, value, optional=None, label=None, help=None,
    #         min=None, max=None, **kwargs):
    #     super(_NumericParam, self).__init__(**params)


class IntegerParam(_NumericParam):
    type = 'int'


class FloatParam(_NumericParam):
    type = 'float'


class BooleanParam(InputParam):
    type = 'boolean'

class ArrayParam(InputParam):
    type = 'array'

class DataParam(InputParam):
    def __init__(self, **kwargs):
        self.type = 'File'
        super(DataParam, self).__init__(**kwargs)


class CWLTool(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description.replace('\n', '\n  ')
        env = Environment(
            loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))),
            trim_blocks=True,
            lstrip_blocks=True)
        self.template = env.get_template('cwltool_inputs.j2')
        self.inputs = []
        self.outputs = []

    def export(self):
        return self.template.render(tool=self,
                                    basecommand='python')
