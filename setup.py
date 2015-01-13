from setuptools import setup, find_packages
import sys, os

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


setup(name="gxargparse",
        version='0.1.9',
        description='Galaxy drop-in replacement for argparse',
        author='Eric Rasche',
        author_email='rasche.eric@yandex.ru',
        requires=['galaxyxml'],
        url='https://github.com/erasche/gxargparse',
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
        )
