import galaxyxml.tool.parameters as gxtp

class ArgparseTranslation(object):

    def __init__(self):
        self.repeat_count = 0

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

        # Positional arguments don't have an option strings
        positional = len(param.option_strings) == 0

        if not positional:
            flag = param.option_strings[0]  # Pick one of the options strings
        else:
            flag = ''

        repeat_name = 'repeat_%s' % self.repeat_count
        repeat_var_name = 'repeat_var_%s' % self.repeat_count

        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)


        gxrepeat_args = []
        gxrepeat_kwargs = {}
        gxrepeat_cli_after = ''
        gxrepeat_cli_before = ''
        if isinstance(param.nargs, int):
            # N (an integer). N arguments from the command line will be
            # gathered together into a list. For example:
            gxrepeat_args = [repeat_name, 'repeat_title']
            gxrepeat_kwargs = {
                    'min': params.nargs,
                    'max': params.nargs,
                    }
            #gxrepeat_cli_after = ''
            #gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var) for $var in $%s ])""" % (repeat_var_name, repeat_name)
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
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var) for $var in $%s ])""" % (repeat_var_name, repeat_name)
        elif param.nargs == '+':
            # '+'. Just like '*', all command-line args present are gathered
            # into a list. Additionally, an error message will be generated if
            # there wasn't at least one command-line argument present. For
            # example:
            gxrepeat_args = [repeat_name, 'repeat_title']
            gxrepeat_kwargs = {'min': 1}
            gxrepeat_cli_after = ''
            gxrepeat_cli_before = """\n#set %s = '" "'.join([ str($var) for $var in $%s ])""" % (repeat_var_name, repeat_name)
        else:
            raise Exception("TODO: Handle argparse.REMAINDER")

        # Build the gxrepeat if it's needed
        if gxrepeat_args is not None:
            gxrepeat = gxtp.Repeat(*gxrepeat_args, **gxrepeat_kwargs)
            gxrepeat.cli_before = gxrepeat_cli_before
            gxrepeat.cli_after = gxrepeat_cli_after
        else:
            gxrepeat = None

        if param.type == int:
            gxparam = gxtp.IntegerParam(flag_wo_dashes, 0, label=param.help,
                    num_dashes=num_dashes)
        elif param.type == float:
            gxparam = gxtp.FloatParam(flag_wo_dashes, 0, label=param.help,
                    num_dashes=num_dashes)
        elif param.type == None or param.type == str:
            gxparam = gxtp.TextParam(flag_wo_dashes, label=param.help,
                    num_dashes=num_dashes)
        elif param.type == file:
            gxparam = gxtp.DataParam(flag_wo_dashes, label=param.help,
                    num_dashes=num_dashes)
        else:
            pass

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
        gxparam = self._StoreConstAction(param, **kwargs)
        gxrepeat = gxtp.Repeat('repeat', 'Repeated Variable')
        gxrepeat.append(gxparam)
        return gxrepeat


    def _StoreConstAction(self, param, **kwargs):
        flag = param.option_strings[0]  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        gxparam = gxtp.BooleanParam(flag_wo_dashes, label=param.help,
                num_dashes=num_dashes)

        return gxparam
