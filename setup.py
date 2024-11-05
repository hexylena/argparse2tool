from setuptools import setup

from argparse2tool import __version__

with open("README.rst") as fh:
    readme = fh.read()

setup(
    name="argparse2tool",
    version=__version__,
    description="Instrument for forming Galaxy XML and CWL tool descriptions from argparse arguments",
    author="Helena Rasche, Anton Khodak",
    author_email="hexylena@galaxians.org",
    long_description=readme,
    long_description_content_type="text/x-rst",
    install_requires=["galaxyxml==0.4.6", "jinja2"],
    url="https://github.com/hexylena/argparse2tool",
    packages=[
        "argparse2tool",
        "argparse2tool.dropins.argparse",
        "argparse2tool.dropins.click",
        "argparse2tool.cmdline2gxml",
        "argparse2tool.cmdline2cwl",
    ],
    entry_points={
        "console_scripts": ["argparse2tool = argparse2tool.check_path:main"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
    ],
    include_package_data=True,
    data_files=[("", ["LICENSE.TXT"])],
)
