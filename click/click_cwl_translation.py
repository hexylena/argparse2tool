import sys

import click
from argparse2tool.cmdline2cwl import cwl_tool as cwlt

PY_TO_CWL_TYPES = {
    'str': 'string',
    'bool': 'boolean',
    'int': 'int',
    'float': 'float',
    'list': 'array',
    'TextIOWrapper': 'File',
    'open': 'File'
}

CLICK_TO_CWL_TYPES = {
    'integer': 'int',
    'text': 'string',
    'choice': 'enum',
    'integer range': 'array',
    'float range': 'array',
    'float': 'float',
    'boolean': 'boolean',
    'uuid': 'string',
    'filename': 'File',
    'file': 'File',
    'directory': 'Directory',
    'path': 'string'
}


class ClickCWLTranslation:
    def __init__(self, generate_outputs=False):
        self.positional_count = 0
        # generate_outputs option allows to form output arguments in CWL tool description from arguments
        # which merely contain keyword `output` in their name
        # Example: parser.add_argument('--output-file', help='some file for output') will be placed into
        # output section (normally only files with FileType('w') are placed into output section
        # However, such behaviour is tricky as '--output-directory' argument will also be treated like File
        # so check generated tools carefully if you choose this option
        self.generate_outputs = generate_outputs

    def __cwl_param_from_type(self, param):
        """Based on a type, convert to appropriate cwlt class
        """
        if param.default == sys.stdout:
            param.default = None
        if hasattr(param, 'optional'):
            optional = param.optional
        else:
            optional = False
        if not hasattr(param, 'items_type'):
            param.items_type = None
        prefix = None
        position = None
        if param.param_type_name == 'option':
            prefix = param.opts[-1]
        if not param.required:
            optional = True
        else:
            self.positional_count += 1
            position = self.positional_count
        param_type = self.get_cwl_type(param.type) or 'str'
        kwargs_positional = {'id': param.name,
                             'position': position,
                             'description': getattr(param, 'help', param.human_readable_name),
                             'default': param.default,
                             'prefix': prefix,
                             'optional': optional,
                             'items_type': param.items_type,
                             'type': param_type}

        if type(param.type) is click.Choice:
            kwargs_positional['choices'] = param.type.choices
        if (isinstance(param.type, click.types.File) and 'w' in param.type.mode) \
                or (self.generate_outputs and 'output' in param.dest):
            cwlparam = cwlt.OutputParam(**kwargs_positional)
        else:
            cwlparam = cwlt.Param(**kwargs_positional)
        return cwlparam

    def __args_from_nargs(self, param):
        if param.nargs == '-1':
            param.items_type = self.get_cwl_type(param.type)
            param.type = list
        return param

    def get_cwl_param(self, param):
        param = self.__args_from_nargs(param)
        cwlparam = self.__cwl_param_from_type(param)
        return cwlparam

    @staticmethod
    def get_cwl_type(py_type):
        if py_type is None:
            return None
        elif isinstance(py_type, click.types.ParamType):
            if isinstance(py_type, click.types.Tuple):
                return str(list(map(lambda click_type: CLICK_TO_CWL_TYPES[click_type.name], py_type.types))).strip('[]')
            cwl_type = CLICK_TO_CWL_TYPES[py_type.name]
            return cwl_type
        else:
            return PY_TO_CWL_TYPES[py_type.__name__]
