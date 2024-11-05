"""Stub for argparse2tool"""

import sys

try:
    from builtins import range
except Exception:
    pass


__version__ = "0.5.2"


def load_argparse():
    ARGPARSE_NUMBER = 1
    return load_conflicting_package(
        "argparse", "argparse2tool/dropins", ARGPARSE_NUMBER
    )


def load_click():
    CLICK_NUMBER = 5
    return load_conflicting_package("click", "argparse2tool/dropins", CLICK_NUMBER)


def load_conflicting_package(name, not_name, module_number):
    """Load a conflicting package
    Some assumptions are made, namely that your package includes the "official"
    one as part of the name. E.g. argparse2tool/argparse, you would call this with:

        >>> real_argparse = load_conflicting_package('argparse', 'argparse2tool', 1)

     http://stackoverflow.com/a/6032023
    """
    import importlib.util
    import importlib.machinery

    for i in range(0, 100):
        random_name = f"random_name_{i}"
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
            spec = importlib.machinery.PathFinder.find_spec(name, [path])
            if spec is None or spec.origin is None:
                continue

            # Check if this is the module we want (avoiding the override)
            if not_name not in spec.origin and isinstance(
                spec.loader, importlib.machinery.SourceFileLoader
            ):
                spec.loader.name = random_name
                spec.name = random_name
                module = importlib.util.module_from_spec(spec)
                sys.modules[random_name] = module
                spec.loader.exec_module(module)
                return sys.modules[random_name]
        except ImportError:
            continue
    return None
