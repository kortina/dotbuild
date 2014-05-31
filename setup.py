import codecs
import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

setup(
    name="dotbuild",
    version=find_version("dotbuild", "__init__.py"),
    description="makes managing dotfiles more standardized and modular",
    long_description=long_description,
    keywords=['dotbuild', 'dotfiles'],
    author='Andrew Kortina',
    author_email='kortina@gmail.com',
    url='https://github.com/kortina/dotbuild',
    license='MIT',
    packages=find_packages(exclude=["contrib", "docs", "tests*", "tasks"]),
    entry_points={
        "console_scripts": [
            "dotbuild=dotbuild.__main__:main",
        ],
    }
)
