from setuptools import setup


setup(name="gxargparse",
        version='0.1.3',
        description='Galaxy drop-in replacement for argparse',
        author='Eric Rasche',
        author_email='rasche.eric@yandex.ru',
        license='GPL3',
        requires=['galaxyxml'],
        url='https://github.com/erasche/gxargparse',
        packages=["argparse"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Environment :: Console',
            ],
        )
