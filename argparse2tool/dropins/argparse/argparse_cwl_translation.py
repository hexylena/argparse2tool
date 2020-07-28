import sys
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


class ArgparseCWLTranslation:

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
        from argparse import FileType
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
                             'items_type': param.items_type,
                             'type': self.get_cwl_type(param.type) or 'string'}

        if param.choices is not None:
            kwargs_positional['choices'] = param.choices
            kwargs_positional['type'] = 'enum'
        if (isinstance(param.type, FileType) and 'w' in param.type._mode) \
                or (self.generate_outputs and 'output' in param.dest):
            cwlparam = cwlt.OutputParam(**kwargs_positional)
        else:
            cwlparam = cwlt.Param(**kwargs_positional)
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
        param = self.__args_from_nargs(param)
        cwlparam = self.__cwl_param_from_type(param)
        return cwlparam

    def _StoreTrueAction(self, param):
        return self.__StoreBoolAction(param)

    def _StoreFalseAction(self, param):
        return self.__StoreBoolAction(param)

    def _AppendAction(self, param, **kwargs):
        param.items_type = self.get_cwl_type(param.type)
        param.type = list
        cwlparam = self.__cwl_param_from_type(param)
        cwlparam.items_type = param.items_type
        return cwlparam

    def _AppendConstAction(self, param):
        """
        AppendConst argument is formed once from `dest` field. `Const` option is ignored
        and must be provided again in job.json
        """
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
        """
        converts given Python type to a CWL type
        >>> ArgparseCWLTranslation.get_cwl_type(list)
        'array'
        """
        if py_type is None:
            return None
        if type(py_type) is type:
            return PY_TO_CWL_TYPES[py_type.__name__]
        elif type(py_type).__name__ == 'builtin_function_or_method' or type(py_type).__name__ == 'FileType':
            return 'File'
        else:  # type given as a string: 'str', 'int' etc.
            return PY_TO_CWL_TYPES.get(py_type, None)
