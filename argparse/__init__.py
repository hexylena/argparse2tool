import sys

# Per @jmchilton's suggestion, and this SO question:
# http://stackoverflow.com/a/6032023
def copy_in_standard_module_symbols(name, not_name, local_module):
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
    correct_sys_path = []
    for path in sys.path:
        try:
            (f, pathname, desc) = imp.find_module(name, [path])
            if not_name not in pathname:
                correct_sys_path = pathname
                handle.close()
                break
        except:
            # Many sys.paths won't contain the module of interest
            pass

    module = imp.load_module(random_name, f, pathname, desc)
    f.close()
    return sys.modules[random_name]

ap = copy_in_standard_module_symbols('argparse', 'gxargparse', sys.modules[copy_in_standard_module_symbols.__module__])
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
import argparse_translation as at

class ArgumentParser(object):

    def __init__(self, *args, **kwargs):
        self.parser = ap.ArgumentParser(*args, **kwargs)
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

