from setuptools import setup

requirements = [x.strip() for x in open('requirements.txt', 'r').readlines()]

setup(name="gxargparse",
        version='0.1',
        description='Galaxy drop-in replacement for argparse',
        author='Eric Rasche',
        author_email='rasche.eric@yandex.ru',
        license='GPL3',
        requires=requirements,
        url='https://github.com/erasche/gxargparse',
        packages=["argparse"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Environment :: Console',
            ],
        )
