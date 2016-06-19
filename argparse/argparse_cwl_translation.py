from __future__ import absolute_import
from builtins import object

import sys

from . import cwl_tool as cwlt

PY_TO_CWL_TYPES = {
    'str': 'string',
    'bool': 'boolean',
    'int': 'int',
    'float': 'float',
    'list': 'array',
    'TextIOWrapper': 'File',
    'open': 'File'

}

class ArgparseCWLTranslation(object):

    def __init__(self, generate_outputs=False):
        self.positional_count = 0
        self.generate_outputs = generate_outputs

    def __cwl_param_from_type(self, param):
        from argparse import FileType
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
        if param.option_strings:
            prefix = param.option_strings[-1]
            if not param.required:
                optional = True
        if param.option_strings:
            position = None
        else:
            self.positional_count += 1
            position = self.positional_count
        kwargs_positional = {'id': param.dest,
                             'position': position,
                             'description': param.help,
                             'default': param.default,
                             'prefix': prefix,
                             'optional': optional,
                             'items_type': param.items_type}

        if param.choices is not None:
            kwargs_positional['choices'] = param.choices
            cwlparam = cwlt.ChoiceParam(**kwargs_positional)
        elif param.type == bool:
            cwlparam = cwlt.BooleanParam(**kwargs_positional)
        elif param.type == list:
            cwlparam = cwlt.ArrayParam(**kwargs_positional)
        elif param.type == int:
            cwlparam = cwlt.IntegerParam(**kwargs_positional)
        elif param.type == float:
            cwlparam = cwlt.FloatParam(**kwargs_positional)
        elif param.type == None or param.type == str:
            if self.generate_outputs and 'output' in param.dest:
                cwlparam = cwlt.OutputParam(**kwargs_positional)
            else:
                cwlparam = cwlt.TextParam(**kwargs_positional)
        elif  type(param.type).__name__ =='builtin_function_or_method' or (isinstance(param.type, FileType) and 'r' in param.type._mode):
            cwlparam = cwlt.FileParam(**kwargs_positional)
        elif isinstance(param.type, FileType) and 'w' in param.type._mode:
            cwlparam = cwlt.OutputParam(**kwargs_positional)
        else:
            cwlparam = None
        return cwlparam


    def __args_from_nargs(self, param):
        if param.nargs:
            if not param.nargs == '?':
                param.items_type = self.get_cwl_type(param.type)
                param.type = list

            if param.nargs == '?' or param.nargs == '*':
                param.optional = True
                param.required = False

        return param

    def _StoreAction(self, param):
        """
        Parse argparse arguments action type of "store", the default.

        param: argparse.Action
        """
        cwlparam = None
        param = self.__args_from_nargs(param)
        cwlparam = self.__cwl_param_from_type(param)
        return cwlparam


    def _StoreTrueAction(self, param):
        return self.__StoreBoolAction(param)

    def _StoreFalseAction(self, param):
        return self.__StoreBoolAction(param)

    def _AppendAction(self, param, **kwargs):
        cwlparam = None
        param.items_type = self.get_cwl_type(param.type)
        param.type = list
        cwlparam = self.__cwl_param_from_type(param)
        cwlparam.items_type = param.items_type
        return cwlparam

    def _AppendConstAction(self, param):
        param.type = list
        param.optional = True
        cwlparam = self.__cwl_param_from_type(param)
        return cwlparam

    def __StoreBoolAction(self, param):
        param.type = bool
        cwlparam = self.__cwl_param_from_type(param)
        return cwlparam

    @staticmethod
    def get_cwl_type(py_type):
        if py_type is None:
            return None
        return PY_TO_CWL_TYPES[py_type.__name__]
