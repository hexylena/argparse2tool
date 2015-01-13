from setuptools import setup, find_packages
import sys

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(name="gxargparse",
        version='0.1.7',
        description='Galaxy drop-in replacement for argparse',
        author='Eric Rasche',
        author_email='rasche.eric@yandex.ru',
        requires=['galaxyxml'],
        url='https://github.com/erasche/gxargparse',
        packages=["argparse"],
        entry_points={
            'console_scripts': [
                    'gxargparse_check_path = argparse.check_path:main',
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
