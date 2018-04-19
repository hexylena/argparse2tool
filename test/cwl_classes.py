from yaml import load
from collections import OrderedDict


class InputBinding:
    def __init__(self, ib):
        self.position = ib.get('position', None)
        self.prefix = ib.get('prefix', None)


class OutputBinding:
    def __init__(self, ob):
        self.glob = ob.get('glob', None)


class Param(object):

    def __init__(self, param):
        self.id = param['id']
        self.type = param.get('type', None)
        self.description = param.get('doc', param.get('description', None))


class InputParam(Param):

    def __init__(self, param):
        super(InputParam, self).__init__(param)
        if type(self.type) is list and self.type[0] == 'null':
            self.optional = True
        else:
            self.optional = False
        self.default = param.get('default', None)
        input_binding = param.get('inputBinding', None)
        if input_binding:
            self.input_binding = InputBinding(input_binding)


class OutputParam(Param):

    def __init__(self, param):
        super(OutputParam, self).__init__(param)
        output_binding = param.get('outputBinding', None)
        if output_binding:
            self.output_binding = OutputBinding(output_binding)


class Tool:

    def __init__(self, filename):

        with open(filename) as f:
            tool = load(f)
        self.tool_class = tool['class']
        if self.tool_class != 'CommandLineTool':
            raise ValueError('Wrong tool class')
        self.basecommand = tool['baseCommand']
        self.inputs = OrderedDict()
        if type(tool['inputs']) is list:  # ids not mapped
            for param_dict in tool['inputs']:
                param = InputParam(param_dict)
                self.inputs[param.id] = param
        elif type(tool['inputs']) is dict:  # ids mapped
            for id, param_dict in tool['inputs'].items():
                param_dict['id'] = id
                param = InputParam(param_dict)
                self.inputs[id] = param
        self.outputs = OrderedDict()
        if tool['outputs']:
            if type(tool['outputs']) is list:  # ids not mapped
                for param_dict in tool['outputs']:
                    param = OutputParam(param_dict)
                    self.outputs[param.id] = param
            elif type(tool['outputs']) is dict:  # ids mapped
                for id, param_dict in tool['outputs'].items():
                    param_dict['id'] = id
                    param = OutputParam(param_dict)
                    self.outputs[id] = param
        self.description = tool.get('doc', tool.get('description', ''))
        self.cwl_version = tool.get('cwlVersion', '')

