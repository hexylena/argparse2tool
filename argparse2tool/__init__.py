"""Stub for argparse2tool"""
import sys
try:
    from builtins import range
except Exception:
    pass


__version__ = '0.4.4'


def load_argparse():
    ARGPARSE_NUMBER = 1
    return load_conflicting_package('argparse', 'argparse2tool', ARGPARSE_NUMBER)


def load_conflicting_package(name, not_name, module_number):
    """Load a conflicting package
    Some assumptions are made, namely that your package includes the "official"
    one as part of the name. E.g. argparse2tool/argparse, you would call this with:

        >>> real_argparse = load_conflicting_package('argparse', 'argparse2tool', 1)

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
            if not_name not in pathname and desc[2] == module_number:
                imp.load_module(random_name, f, pathname, desc)
                return sys.modules[random_name]
        except Exception:
            # Many sys.paths won't contain the module of interest
            pass
    return None
