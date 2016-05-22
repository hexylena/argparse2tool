from __future__ import absolute_import
from builtins import object

from io import IOBase

import sys

from . import cwl_tool as cwlt


class ArgparseCWLTranslation(object):

    def __init__(self):
        self.positional_count = 0

    def __cwl_param_from_type(self, param, position, default=None):
        from argparse import FileType
        """Based on a type, convert to appropriate cwlt class
        """
        if default is None and (param.type in (int, float)):
            default = 0
        elif default == sys.stdout:
            default = None
        kwargs_positional = {'id': param.dest,
                             'position': position,
                             'description': param.help,
                             'default': default}

        if param.choices is not None:
            pass
        elif param.type == bool:
            cwlparam = cwlt.BooleanParam(**kwargs_positional)
        elif param.type == list:
            cwlparam = cwlt.ArrayParam(**kwargs_positional)
        elif param.type == int:
            cwlparam = cwlt.IntegerParam(**kwargs_positional)
        elif param.type == float:
            cwlparam = cwlt.FloatParam(**kwargs_positional)
        elif param.type == None or param.type == str:
            cwlparam = cwlt.TextParam(**kwargs_positional)
        elif isinstance(param.type, IOBase):
            pass
        elif isinstance(param.type, FileType):
            if 'w' in param.type._mode:
                cwlparam = cwlt.OutputParam(**kwargs_positional)
            else:
                # don't know what other types except frofm `file` can be in DataParam, but let it be for now
                cwlparam = cwlt.DataParam(**kwargs_positional)
        else:
            cwlparam = None
        return cwlparam


    def _StoreAction(self, param,):
        """
        Parse argparse arguments action type of "store", the default.

        param: argparse.Action
        """
        cwlparam = None
        self.positional_count += 1
        cwlparam = self.__cwl_param_from_type(param, self.positional_count, default=param.default)

        return cwlparam


    def _StoreTrueAction(self, param, **kwargs):
        return self._StoreConstAction(param, **kwargs)

    def _StoreFalseAction(self, param, **kwargs):
        return self._StoreConstAction(param, **kwargs)

    def _AppendAction(self, param, **kwargs):
        cwlparam = None
        self.positional_count += 1
        param.items_type = param.type
        param.type = list
        cwlparam = self.__cwl_param_from_type(param, self.positional_count, default=param.default)
        cwlparam.items_type = param.items_type
        return cwlparam


    def _StoreConstAction(self, param, **kwargs):
        self.positional_count += 1
        cwlparam = self.__cwl_param_from_type(param, self.positional_count)
        return cwlparam
