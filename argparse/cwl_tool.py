import os

from jinja2 import Environment, FileSystemLoader


class Param(object):
    def __init__(self, id, position):
        self.id = id
        self.position = position


class TextParam(Param):
    def __init__(self, **kwargs):
        self.type = 'string'
        super(TextParam, self).__init__(**kwargs)


class DataParam(Param):
    def __init__(self, **kwargs):
        self.type = 'File'
        super(DataParam, self).__init__(**kwargs)


class CWLTool(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))))
        self.template = env.get_template('cwltool_inputs.j2')
        self.inputs = []

    def export(self):
        return self.template.render(tool=self,
                                    basecommand='python')
