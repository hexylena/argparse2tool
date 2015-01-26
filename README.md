# `gxargparse`

Galaxy argparse aims to be a drop-in replacement for argparse, quite literally.
You can write use your normal import

```python
import argparse
```

and continue writing code. All functions are passed straight through to
argparse, but `gxargparse` captures them and copies some information along the
way. This information captured is used to produce [Galaxy Tool XML](https://github.com/erasche/galaxyxml) when it's
requested with the `--generate_galaxy_xml` flag.

## How it works

Internally, `gxargparse`, masquerading as `argparse` attempts to find and
import the **real** argparse. It then stores a reference to the code module for
the system argparse, and presents the user with all of the functions that
stdlib's argparse provides. Every function call is passed through the system
argparse. However, gxargparse captures the details of those calls and when Tool
XML is requested, it builds up the tool definition according to IUC tool
standards.

## Examples

You can see the `example.py` file for an example with numerous types of
arguments and options that you might see in real tools. Accordingly there is an `example.xml` file with the output.

## It doesn't work!!

If you are not able to use the `--generate_galaxy_xml` flag after
installing, it is probably because of module load order. gxargparse must
precede argparse in the path. Certain cases seem to work correctly (`python
setup.py install` in a virtualenv) while other cases do not (`pip install
gxargparse`).

To easily correct this, run the tool `gxargparse_check_path` which is installed
as part of this package. Correctly functioning paths will produce the
following:

```console
$ gxargparse_check_path
Ready to go!
```

while incorrectly ordered paths will produce a helpful error message:

```console
$ gxargparse_check_path
Incorrect ordering, please set

    PYTHONPATH=/home/users/esr/Projects/test/.venv/local/lib/python2.7/site-packages

```

## TODO

This code doesn't cover the entirety of the `argparse` API yet, and there are some bugs to work out on the XML generation side:

- argparse
    - groups not supported (in galaxy, everything should still work in argparse)
    - some features like templating of the version string (please submit bugs)
- galaxyxml
    - bugs in conditionals/whens (probably)
    - bugs, bugs, bugs!
- gxargparse
    - support help text
    - support declaring output files in an `argparse`-esque manner

# License

- Apache License, v2
