import galaxyxml.tool.parameters as gxtp

class ArgparseTranslation(object):

    def _VersionAction(self, param, tool=None):
        # passing tool is TERRIBLE, I know.
        # TODO handle their templating of version

        # This is kinda ugly but meh.
        tool.root.attrib['version'] = param.version


    def _StoreAction(self, param, tool=None):
        gxparam = None
        gxrepeat = None
        if len(param.option_strings) == 0:
            # Positional argument, yikes
            flag = ''
        else:
            flag = param.option_strings[0]  # Pick one of the options strings
        flag_wo_dashes = flag.lstrip('-')
        num_dashes = len(flag) - len(flag_wo_dashes)

        if isinstance(param.nargs, int):
            # N (an integer). N arguments from the command line will be
            # gathered together into a list. For example:
            gxrepeat = gxtp.Repeat('repeat_name', 'repeat_title',
                    min=param.nargs, max=param.nargs)
            gxrepeat.cli_after = ''
            gxrepeat.cli_before = """\n#set repeat_var = '" "'.join([ str($var) for $var in $repeat_name ])"""
        elif param.nargs == '?':
            # '?'. One argument will be consumed from the command line if
            # possible, and produced as a single item. If no command-line
            # argument is present, the value from default will be produced
            gxrepeat = None
        elif param.nargs == '*':
            # '*'. All command-line arguments present are gathered into a list.
            # Note that it generally doesn't make much sense to have more than
            # one positional argument with nargs='*', but multiple optional
            # arguments with nargs='*' is possible. For example:

            # This needs to be handled with a
            #set files = '" "'.join( [ str( $file ) for $file in $inputB ] )
            gxrepeat = gxtp.Repeat('repeat_name', 'repeat_title')
            gxrepeat.cli_after = ''
            gxrepeat.cli_before = """\n#set repeat_var = '" "'.join([ str($var) for $var in $repeat_name ])"""
        elif param.nargs == '+':
            # '+'. Just like '*', all command-line args present are gathered
            # into a list. Additionally, an error message will be generated if
            # there wasn't at least one command-line argument present. For
            # example:
            gxrepeat = gxtp.Repeat('repeat_name', 'repeat_title', min=1)
            gxrepeat.cli_after = ''
            gxrepeat.cli_before = """\n#set repeat_var = '" "'.join([ str($var) for $var in $repeat_name ])"""
        else:
            raise Exception("TODO: Handle argparse.REMAINDER")

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
