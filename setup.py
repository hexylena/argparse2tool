import os
import sys

from setuptools import setup

from argparse2tool import __version__

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload; git push")
    sys.exit()

setup(name="argparse2tool",
        version=__version__,
        description='Instrument for forming Galaxy XML and CWL tool descriptions from argparse arguments',
        author='Eric Rasche, Anton Khodak',
        author_email='esr@tamu.edu, anton.khodak@ukr.net',
        install_requires=['galaxyxml>=0.2.3', 'jinja2', 'future'],
        url='https://github.com/erasche/argparse2tool',
        packages=["argparse", "argparse2tool", "click", "argparse2tool.cmdline2gxml", "argparse2tool.cmdline2cwl"],
        entry_points={
            'console_scripts': [
                    'argparse2tool_check_path = argparse2tool.check_path:main',
                ]
            },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'License :: OSI Approved :: Apache Software License',
            ],
        include_package_data=True,
        )
