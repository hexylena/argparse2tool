import sys
import argparse
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
import argparse_translation as at

class ArgumentParser(object):

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(*args, **kwargs)
        #print dir(self.parser)
        self.argument_list = []
        #print self.parser.prefix_chars

    def add_argument(self, *args, **kwargs):
        result = self.parser.add_argument(*args, **kwargs)
        self.argument_list.append(result)

    def parse_args(self, *args, **kwargs):
        if '--generate_galaxy_xml' in sys.argv:
            self.tool = gxt.Tool(
                    self.parser.prog,
                    self.parser.prog,
                    self.parser.print_version(),
                    self.parser.description,
                    self.parser.prog)

            self.inputs = gxtp.Inputs()
            self.outputs = gxtp.Outputs()
            self.at = at.ArgparseTranslation()
            # Only build up arguments if the user actually requests it
            for result in self.argument_list:
                # I am SO thankful they return the argument here. SO useful.
                argument_type = result.__class__.__name__
                # http://stackoverflow.com/a/3071
                methodToCall = getattr(self.at, argument_type)
                gxt_parameter = methodToCall(result, tool=self.tool)
                if gxt_parameter is not None:
                    self.inputs.append(gxt_parameter)

            self.tool.inputs = self.inputs
            self.tool.outputs = self.outputs
            self.tool.help = 'HI'
            data = self.tool.export()
            print data
            sys.exit()
        else:
            return self.parser.parse_args(*args, **kwargs)

