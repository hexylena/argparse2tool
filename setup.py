import os
import sys

from setuptools import setup

import argparse

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload; git push")
    sys.exit()

setup(name="gxargparse",
        version=argparse.__version__,
        description='Instrument for forming Galaxy XML and CWL tool descriptions from argparse arguments',
        author='Eric Rasche, Anton Khodak',
        author_email='rasche.eric@yandex.ru, anton.khodak@ukr.net',
        install_requires=['galaxyxml', 'jinja2', 'future'],
        url='https://github.com/common-workflow-language/gxargparse',
        packages=["argparse", "gxargparse"],
        entry_points={
            'console_scripts': [
                    'gxargparse_check_path = gxargparse.check_path:main',
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
