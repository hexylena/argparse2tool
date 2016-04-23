import sys

from argparse.cwl_tool import CWLTool


def load_conflicting_package(name, not_name, local_module):
    """Load a conflicting package

    Some assumptions are made, namely that your package includes the "official"
    one as part of the name. E.g. gxargparse/argparse, you would call this with:

        >>> real_argparse = load_conflicting_package('argpargase', 'gxargparse',
        ...                                          sys.modules[load_conflicting_package.__module__])

     http://stackoverflow.com/a/6032023
    """
    import imp

    for i in range(0, 100):
        random_name = 'random_name_%d' % (i,)
        if random_name not in sys.modules:
            break
        else:
            random_name = None
    if random_name is None:
        raise RuntimeError("Couldn't manufacture an unused module name.")
    # NB: This code is unlikely to work for nonstdlib overrides.
    # This will hold the correct sys.path for the REAL argparse
    for path in sys.path:
        try:
            (f, pathname, desc) = imp.find_module(name, [path])
            if not_name not in pathname and desc[2] == 1:
                module = imp.load_module(random_name, f, pathname, desc)
                f.close()
                return sys.modules[random_name]
        except:
            # Many sys.paths won't contain the module of interest
            pass
    return None

ap = load_conflicting_package('argparse', 'gxargparse', sys.modules[load_conflicting_package.__module__])
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
import argparse_galaxy_translation as agt
import argparse_cwl_translation as act
import cwl_tool as cwlt

# This fetches a reference to ourselves
__selfmodule__ = sys.modules[load_conflicting_package.__module__]
# Static list of imports
__argparse_exports__ = ['HelpFormatter', 'RawDescriptionHelpFormatter',
                        'ArgumentDefaultsHelpFormatter', 'FileType',
                        'SUPPRESS', 'OPTIONAL', 'ZERO_OR_MORE', 'ONE_OR_MORE',
                        'PARSER', 'REMAINDER', '_UNRECOGNIZED_ARGS_ATTR',
                        '_VersionAction']

# Set the attribute on ourselves.
for x in __argparse_exports__:
    setattr(__selfmodule__, x, getattr(ap, x))


class ArgumentParser(ap.ArgumentParser):

    argument_list = []

    def add_argument(self, *args, **kwargs):
        result = ap.ArgumentParser.add_argument(self, *args, **kwargs)
        self.argument_list.append(result)

    def parse_args(self, *args, **kwargs):
        if '--generate_cwl_tool' in sys.argv:
            self.parse_args_cwl(*args, **kwargs)
        elif '--generate_galaxy_xml' in sys.argv:
            self.parse_args_galaxy_nouse(*args, **kwargs)
        else:
            return ap.ArgumentParser.parse_args(self, *args, **kwargs)

    def parse_args_cwl(self, *args, **kwargs):
        self.tool = cwlt.CWLTool(self.prog, self.description)
        self.at = act.ArgparseCWLTranslation()
        # Only build up arguments if the user actually requests it
        for result in self.argument_list:
            argument_type = result.__class__.__name__
            # http://stackoverflow.com/a/3071
            if hasattr(self.at, argument_type):
                methodToCall = getattr(self.at, argument_type)
                cwlt_parameter = methodToCall(result)
                if cwlt_parameter is not None:
                    if isinstance(cwlt_parameter, cwlt.Param):
                        self.tool.inputs.append(cwlt_parameter)

        if self.epilog is not None:
            self.tool.help = self.epilog
        else:
            self.tool.help = "TODO: Write help"

        data = self.tool.export()
        print data
        sys.exit()

    def parse_args_galaxy_nouse(self, *args, **kwargs):
        self.tool = gxt.Tool(
                self.prog,
                self.prog,
                self.print_version() or '1.0',
                self.description,
                self.prog,
                interpreter='python',
                version_command='python %s --version' % sys.argv[0])

        self.inputs = gxtp.Inputs()
        self.outputs = gxtp.Outputs()

        self.at = agt.ArgparseGalaxyTranslation()
        # Only build up arguments if the user actually requests it
        for result in self.argument_list:
            # I am SO thankful they return the argument here. SO useful.
            argument_type = result.__class__.__name__
            # http://stackoverflow.com/a/3071
            if hasattr(self.at, argument_type):
                methodToCall = getattr(self.at, argument_type)
                gxt_parameter = methodToCall(result, tool=self.tool)
                if gxt_parameter is not None:
                    if isinstance(gxt_parameter, gxtp.InputParameter):
                        self.inputs.append(gxt_parameter)
                    else:
                        self.outputs.append(gxt_parameter)

        # TODO: replace with argparse-esque library to do this.
        stdout = gxtp.OutputParameter('default', 'txt')
        stdout.command_line_override = '> $default'
        self.outputs.append(stdout)

        self.tool.inputs = self.inputs
        self.tool.outputs = self.outputs
        if self.epilog is not None:
            self.tool.help = self.epilog
        else:
            self.tool.help = "TODO: Write help"

        data = self.tool.export()
        print data
        sys.exit()
