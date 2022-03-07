import galaxyxml.tool.parameters as gxtp
from collections import Counter
from pydoc import locate


class ArgparseGalaxyTranslation(object):

    def __gxtp_param_from_type(self, param, flag, label, num_dashes, gxparam_extra_kwargs, default=None):
        from argparse import FileType
        """Based on a type, convert to appropriate gxtp class
        """
        if default is None and (param.type in (int, float)):
            default = 0

        if param.type == int:
            mn = None
            mx = None
            if param.choices is not None:
                mn = min(param.choices)
                mx = max(param.choices)
            gxparam = gxtp.IntegerParam(flag, default, label=label, min=mn, max=mx, num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param.choices is not None:
            choices = {k: k for k in param.choices}
            gxparam = gxtp.SelectParam(flag, default=default, label=label, num_dashes=num_dashes, options=choices, **gxparam_extra_kwargs)
        elif param.type == float:
            gxparam = gxtp.FloatParam(flag, default, label=label, num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param.type is None or param.type == str:
            gxparam = gxtp.TextParam(flag, value=default, label=label, num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param.type == locate('file'):
            gxparam = gxtp.DataParam(flag, label=label, num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif isinstance(param.type, FileType):
            if 'w' in param.type._mode:
                gxparam = gxtp.OutputData(
                    flag, format='data', default=default, label=label,
                    num_dashes=num_dashes, **gxparam_extra_kwargs
                )
            else:
                gxparam = gxtp.DataParam(
                    flag, default=default, label=label, num_dashes=num_dashes,
                    **gxparam_extra_kwargs
                )
        else:
            gxparam = None

        return gxparam

    def __args_from_nargs(self, param, repeat_name, repeat_var_name, positional, flag):
        """Based on param.nargs, return the appropriate overrides
        """
        gxrepeat_args = []
        gxrepeat_kwargs = {}
        gxrepeat_cli_after = None
        gxrepeat_cli_before = None
        gxrepeat_cli_actual = None

        gxparam_cli_before = None
        gxparam_cli_after = None

        if positional:
            gxrepeat_cli_actual = '"$%s"' % (repeat_var_name)
        else:
            gxrepeat_cli_actual = '%s "$%s"' % (param.option_strings[0], repeat_var_name)

        if isinstance(param.nargs, int):
            # N (an integer). N arguments from the command line will be
            # gathered together into a list. For example:
            if param.nargs > 1:
                gxrepeat_args = [repeat_name, 'repeat_title']
                gxrepeat_kwargs = {
                    'min': param.nargs,
                    'max': param.nargs,
                }
            else:
                # If we have only one, we don't want a gxrepeat, so we leave well
                # enough alone
                gxrepeat_args = None
        elif param.nargs == '?':
            # '?'. One argument will be consumed from the command line if
            # possible, and produced as a single item. If no command-line
            # argument is present, the value from default will be produced.
            # Note that for optional arguments, there is an additional case -
            # the option string is present but not followed by a command-line
            # argument. In this case the value from const will be produced

            # This does NOT provide a way to access the value in const, but
            # that seems like a HORRIBLE idea anyway. Seriously, who does that.
            gxparam_cli_before = """\n#if $%s and $%s is not None:""" % (flag, flag)
            gxparam_cli_after = '#end if'

            gxrepeat_args = None
        elif param.nargs is None:
            # Very similar to '?' but without the case of "optional + specified
            # withouth an argument" being OK
            #
            # This has changed over time, we're (probably) going overboard here.
            gxparam_cli_before = """\n#if $%s and $%s is not None:""" % (flag, flag)
            gxparam_cli_after = '#end if'
            gxrepeat_args = None
        elif param.nargs == '*':
            # '*'. All command-line arguments present are gathered into a list.
            # Note that it generally doesn't make much sense to have more than
            # one positional argument with nargs='*', but multiple optional
            # arguments with nargs='*' is possible. For example:

            # This needs to be handled with a
            # set files = '" "'.join( [ str( $file ) for $file in $inputB ] )

            gxrepeat_args = [repeat_name, 'repeat_title']
            # gxrepeat_cli_after = '#end if\n'
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var.%s) for $var in $%s ])""" % (repeat_var_name, flag, repeat_name)
        elif param.nargs == '+':
            # '+'. Just like '*', all command-line args present are gathered
            # into a list. Additionally, an error message will be generated if
            # there wasn't at least one command-line argument present. For
            # example:
            gxrepeat_args = [repeat_name, 'repeat_title']
            gxrepeat_kwargs = {'min': 1}
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var.%s) for $var in $%s ])""" % (repeat_var_name, flag, repeat_name)
        else:
            raise Exception("TODO: Handle argparse.REMAINDER")

        return (gxrepeat_args, gxrepeat_kwargs, gxrepeat_cli_after,
                gxrepeat_cli_before, gxrepeat_cli_actual, gxparam_cli_before, gxparam_cli_after)

    def __init__(self):
        self.repeat_count = 0
        self.positional_count = Counter()

    def _VersionAction(self, param, tool=None):
        # passing tool is TERRIBLE, I know.
        # TODO handle their templating of version

        # This is kinda ugly but meh.
        tool.root.attrib['version'] = param.version

        # Count the repeats for unique names
        # TODO improve

    def _StoreAction(self, param, tool=None):
        """
        Parse argparse arguments action type of "store", the default.

        param: argparse.Action
        """
        gxparam = None
        gxrepeat = None
        self.repeat_count += 1
        gxparam_extra_kwargs = {}

        if not param.required:
            gxparam_extra_kwargs['optional'] = True

        # Positional arguments don't have an option strings
        positional = len(param.option_strings) == 0

        if not positional:
            flag = max(param.option_strings, key=len)  # Pick the longest of the options strings
        else:
            flag = ''
            self.positional_count['param.dest'] += 1

        repeat_name = 'repeat_%s' % self.repeat_count
        repeat_var_name = 'repeat_var_%s' % self.repeat_count

        # TODO: Replace with logic supporting characters other than -
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        # Moved because needed in developing repeat CLI
        if positional:
            v = self.positional_count[param.dest]
            flag_wo_dashes = '%s%s' % (param.dest, '_' + str(v) if v > 1 else '')
            # SO unclean
            gxparam_extra_kwargs['positional'] = True

        # Figure out parameters and overrides from param.nargs, mainly.
        # This is really unpleasant.
        (gxrepeat_args, gxrepeat_kwargs, gxrepeat_cli_after,
         gxrepeat_cli_before, gxrepeat_cli_actual, gxparam_cli_before,
         gxparam_cli_after) = \
            self.__args_from_nargs(param, repeat_name, repeat_var_name, positional, flag_wo_dashes)

        # Build the gxrepeat if it's needed
        if gxrepeat_args is not None:
            gxrepeat = gxtp.Repeat(*gxrepeat_args, **gxrepeat_kwargs)
            if gxrepeat_cli_before is not None:
                gxrepeat.command_line_before_override = gxrepeat_cli_before
            if gxrepeat_cli_after is not None:
                gxrepeat.command_line_after_override = gxrepeat_cli_after
            if gxrepeat_cli_actual is not None:
                gxrepeat.command_line_override = gxrepeat_cli_actual
        else:
            gxrepeat = None

        gxparam = self.__gxtp_param_from_type(
            param, flag_wo_dashes, param.help, num_dashes,
            gxparam_extra_kwargs, default=param.default
        )

        # Not really happy with this way of doing this
        if gxparam_cli_before is not None:
            gxparam.command_line_before_override = gxparam_cli_before

        if gxparam_cli_after is not None:
            gxparam.command_line_after_override = gxparam_cli_after

        # if positional argument, wipe out the CLI flag that's usually present
        if positional:
            gxparam.command_line_override = '$%s' % flag_wo_dashes

        if gxrepeat is not None and gxparam is not None:
            gxrepeat.append(gxparam)
            return gxrepeat
        elif gxrepeat is None and gxparam is not None:
            return gxparam
        else:
            raise Exception("huh")
        return None

    def _StoreTrueAction(self, param, **kwargs):
        return self._StoreConstAction(param, **kwargs)

    def _StoreFalseAction(self, param, **kwargs):
        return self._StoreConstAction(param, **kwargs)

    def _AppendAction(self, param, **kwargs):
        self.repeat_count += 1
        repeat_name = 'repeat_%s' % self.repeat_count
        # TODO: Replace with logic supporting characters other than -
        flag = max(param.option_strings, key=len)  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        gxparam = self.__gxtp_param_from_type(param, flag_wo_dashes, param.help, num_dashes, {})
        gxrepeat = gxtp.Repeat(repeat_name, 'Repeated Variable')
        gxrepeat.command_line_override = '%s $%s.%s' % (param.option_strings[0], 'i', flag_wo_dashes)
        gxrepeat.append(gxparam)
        return gxrepeat

    def _StoreConstAction(self, param, **kwargs):
        flag = max(param.option_strings, key=len)  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        gxparam = gxtp.BooleanParam(flag_wo_dashes, label=param.help, num_dashes=num_dashes)

        return gxparam
