import galaxyxml.tool.parameters as gxtp

class ArgparseTranslation(object):

    def __gxtp_param_from_type(self, param_type, flag, label, num_dashes, gxparam_extra_kwargs, default=0):
        """Based on a type, convert to appropriate gxtp class
        """
        if param_type == int:
            gxparam = gxtp.IntegerParam(flag, default, label=label,
                    num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param_type == float:
            gxparam = gxtp.FloatParam(flag, default, label=label,
                    num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param_type == None or param_type == str:
            gxparam = gxtp.TextParam(flag, label=label,
                    num_dashes=num_dashes, **gxparam_extra_kwargs)
        elif param_type == file:
            gxparam = gxtp.DataParam(flag, label=label,
                    num_dashes=num_dashes, **gxparam_extra_kwargs)
        else:
            gxparam = None

        return gxparam

    def __args_from_nargs(self, param, repeat_name, repeat_var_name, positional, flag):
        """Based on param.nargs, return the appropriate overrides
        """
        gxrepeat_args = []
        gxrepeat_kwargs = {}
        gxrepeat_cli_after = ''
        gxrepeat_cli_before = ''
        gxrepeat_cli_actual = ''

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
            # argument is present, the value from default will be produced
            gxrepeat_args = None
        elif param.nargs == '*':
            # '*'. All command-line arguments present are gathered into a list.
            # Note that it generally doesn't make much sense to have more than
            # one positional argument with nargs='*', but multiple optional
            # arguments with nargs='*' is possible. For example:

            # This needs to be handled with a
            #set files = '" "'.join( [ str( $file ) for $file in $inputB ] )

            gxrepeat_args = [repeat_name, 'repeat_title']
            #gxrepeat_cli_after = '#end if\n'
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var.%s) for $var in $%s ])""" % (repeat_var_name, flag, repeat_name)
            # Gotta be a better way to do this, probably in the param itself?
            if positional:
                gxrepeat_cli_actual = '"$%s"' % (repeat_var_name)
            else:
                gxrepeat_cli_actual = '%s "$%s"' % (param.option_strings[0], repeat_var_name)
        elif param.nargs == '+':
            # '+'. Just like '*', all command-line args present are gathered
            # into a list. Additionally, an error message will be generated if
            # there wasn't at least one command-line argument present. For
            # example:
            gxrepeat_args = [repeat_name, 'repeat_title']
            gxrepeat_kwargs = {'min': 1}
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var.%s) for $var in $%s ])""" % (repeat_var_name, flag, repeat_name)

            if positional:
                gxrepeat_cli_actual = '"$%s"' % repeat_var_name
            else:
                gxrepeat_cli_actual = '%s "$%s"' % (param.option_strings[0], repeat_var_name)
        else:
            raise Exception("TODO: Handle argparse.REMAINDER")


        return (gxrepeat_args, gxrepeat_kwargs, gxrepeat_cli_after,
                gxrepeat_cli_before, gxrepeat_cli_actual)


    def __init__(self):
        self.repeat_count = 0
        self.positional_count = 0

    def _VersionAction(self, param, tool=None):
        # passing tool is TERRIBLE, I know.
        # TODO handle their templating of version

        # This is kinda ugly but meh.
        tool.root.attrib['version'] = param.version

        # Count the repeats for unique names
        # TODO improve


    def _StoreAction(self, param, tool=None):
        gxparam = None
        gxrepeat = None
        self.repeat_count += 1
        gxparam_extra_kwargs = {}

        # Positional arguments don't have an option strings
        positional = len(param.option_strings) == 0

        if not positional:
            flag = param.option_strings[0]  # Pick one of the options strings
        else:
            flag = ''
            self.positional_count += 1

        repeat_name = 'repeat_%s' % self.repeat_count
        repeat_var_name = 'repeat_var_%s' % self.repeat_count

        # TODO: Replace with logic supporting characters other than -
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        # Moved because needed in developing repeat CLI
        if positional:
            flag_wo_dashes = 'positional_%s' % self.positional_count
            # SO unclean
            gxparam_extra_kwargs['positional'] = True


        # Figure out parameters and overrides from param.nargs, mainly.
        (gxrepeat_args, gxrepeat_kwargs, gxrepeat_cli_after,
                gxrepeat_cli_before, gxrepeat_cli_actual) = \
            self.__args_from_nargs(param, repeat_name, repeat_var_name, positional, flag_wo_dashes)


        # Build the gxrepeat if it's needed
        if gxrepeat_args is not None:
            gxrepeat = gxtp.Repeat(*gxrepeat_args, **gxrepeat_kwargs)
            gxrepeat.cli_before = gxrepeat_cli_before
            gxrepeat.cli_after = gxrepeat_cli_after
            gxrepeat.command_line_override = gxrepeat_cli_actual
        else:
            gxrepeat = None


        gxparam = self.__gxtp_param_from_type(param.type, flag_wo_dashes,
                param.help, num_dashes, gxparam_extra_kwargs)

        # if positional argument, wipe out the CLI flag that's usually present
        if positional:
            gxparam.command_line_override = '$%s' % flag_wo_dashes

        if gxrepeat is not None and gxparam is not None:
            pass
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
        flag = param.option_strings[0]  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        gxparam = self.__gxtp_param_from_type(param.type, flag_wo_dashes, param.help, num_dashes, {})
        gxrepeat = gxtp.Repeat(repeat_name, 'Repeated Variable')
        gxrepeat.command_line_override = '%s $%s.%s' % (param.option_strings[0], 'i', flag_wo_dashes)
        gxrepeat.append(gxparam)
        return gxrepeat


    def _StoreConstAction(self, param, **kwargs):
        flag = param.option_strings[0]  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        gxparam = gxtp.BooleanParam(flag_wo_dashes, label=param.help,
                num_dashes=num_dashes)

        return gxparam
