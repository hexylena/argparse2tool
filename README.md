# `gxargparse`

Galaxy argparse aims to be a drop-in replacement for argparse, quite literally.
You can write

```python
import gxargparse as argparse
```

and continue writing code as normal. All functions are passed straight through
to argparse, but gxargparse captures them and copies some information along the
way. This information captured is used to produce [https://github.com/erasche/galaxyxml](Galaxy Tool XML) when it's
requested with the `--generate_galaxy_xml` flag

## How it works

The `add_argument` function behaves transparently, generating tool parameters.
When Tool XML is requested, those parameters are collected and analysed, and
the complex tool XML built up according to IUC tool standards.

## Examples

You can see the `example.py` file for an example with numerous types of
arguments and options that you might see in real tools. Accordingly there is an `example.xml` file with the output.

## TODO

This code doesn't cover the entirety of the `argparse` API yet, and there are some bugs to work out on the XML generation side:

- argparse
    - groups not supported
    - some features like "epilogue" and templating of the version string
- galaxyxml
    - bugs in repeats (and names in general)
    - bugs in conditionals/whens
    - bugs, bugs, bugs!
    - validation of passed arguments/unique parameter names/proper labelling
- gxargparse
    - support help text
    - support declaring output files in an `argparse`-esque manner

# License

GPLv3
