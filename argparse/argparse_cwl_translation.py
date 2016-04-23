import cwl_tool as cwlt


class ArgparseCWLTranslation(object):

    def __init__(self):
        self.positional_count = 0

    def __cwl_param_from_type(self, param, position, default=None):
        from argparse import FileType
        """Based on a type, convert to appropriate cwlt class
        """
        kwargs_positional = {'id': param.dest,
                             'position': position}
        if default is None and (param.type in (int, float)):
            default = 0

        if param.choices is not None:
            pass
        elif param.type == int:
            pass
        elif param.type == float:
            pass
        elif param.type == None or param.type == str:
            cwlparam = cwlt.TextParam(**kwargs_positional)
        elif param.type == file:
            pass
        elif isinstance(param.type, FileType):
            if 'w' in param.type._mode:
                pass
            else:
                # don't know what other types except from `file` can be in DataParam, but let it be for now
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
