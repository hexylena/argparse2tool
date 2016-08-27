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

This can even be used inline:

```console
user@host:$ PYTHONPATH=$(gxargparse_check_path -q) python my_script.py --generate_galaxy_xml
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


# argparse2cwl

`argparse2cwl` forms CWL tool descriptions from programs which use `argparse` as their argument parser. 
No code changes are required, just use the normal import:

	import argparse

and continue writing code. All functions are passed straight through to `argparse`, but `argparse2cwl` captures them and copies some information along the way. This information captured is used to produce CWL tool definition when it's requested with the `--generate_cwl_tool` flag.


## Installing ##

Installation process:

1. Clone the source repository:
	
		$ git clone https://github.com/common-workflow-language/gxargparse.git

2. Run 
		$ cd gxargparse
		$ python setup.py install

You can ensure it's working when you pass `--help_arg2cwl` flag to any command-line program inside your environment. If the option is not recognized, try
	
	$ gxargparse_check_path

which is installed as part of this package. It will produce a helpful error message if the paths are incorrectly ordered. Also make sure you have installed it under proper Python version.


## Running ##

To run `argparse2cwl`, call your tool as usually without actual arguments with `--generate_cwl_tool` option:

	$ <tool command> --generate_cwl_tool <other options>

Simple example
	
	$ python example.py --generate_cwl_tool

Example for [CNVkit](https://github.com/etal/cnvkit) toolkit:

	$ cnvkit.py batch --generate_cwl_tool -d ~/cnvkit-tools/ --generate_outputs


If there are subcommands in the provided command, all possible tools will be generated, for instance, for CNVkit

	$ cnvkit.py --generate_cwl_tool

will produce CWL tool descriptions for `cnvkit.py batch`, `cnvkit.py access`, `cnvkit.py export bed`, `cnvkit.py export cdt` and all other subcommands.


Other options (which work only with `--generate_cwl_tool` provided, except for help message) are:

* `-o FILENAME`, `--output_section FILENAME`: File with manually filled output section which is put to a formed CWL tool. Argparse2cwl is not very good at generating outputs, it recognizes output files only if they have type `argparse.FileType('w')`, so output section is often blank and should be filled manually.

* `-go`, `--generate_outputs`: flag for generating outputs not only from arguments that are instances of `argparse.FileType('w')`, but also from every argument which contains `output` keyword in its name. For instance, argument `--output-file` with no type will also be placed to output section. However, '--output-directory' argument will also be treated like File, so generated tools must be checked carefully if when this option is selected.

* `-b`, `basecommand`: command which appears in `basecommand` field in a resulting tool. It is handy to use this option when you run tool with shebang, but want `python` to be in `basecommand` field and the file amidst arguments. 
Example:

	```$ .search.py --generate_cwl_tool -b python```. 

Basecommand of the formed tool will be `['python']`, and `search` will be a positional argument on position 0.

* `-d`, `--directory`: directory for storing tool descriptions.

* `--help_arg2cwl`: prints this help message.



## Argparse notes ##

Some of argparse features can not be ported to CWL. 

1. `nargs=N`. Number of arguments can not be specified in CWL (yet).
2. `const` argument of `add_argument()`. All constants must be specified in job files.
3. Custom types and custom actions are not supported.
4. Argument groups don't work in CWL as arguments are sorted with a [special algorithm](http://www.commonwl.org/draft-3/CommandLineTool.html#Input_binding)
5. Mutual exclusion is not supported.

#	 click2cwl

*click2cwl* shares absolutely the same logic as argparse2cwl, the only difference is it is adjusted to work with [click](http://click.pocoo.org/) argument parser. Whenever click is imported, gxargparse grabs its commands, arguments, options and forms CWL parameters out of them. 

# License

- Apache License, v2
