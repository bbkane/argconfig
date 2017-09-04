import os
import re
from setuptools import setup

SCRIPT_DIR = os.path.dirname(__file__)


def readme():
    readme_path = os.path.join(SCRIPT_DIR, 'README.rst')
    with open(readme_path) as f:
        return f.read()


def get_version():
    init_path = os.path.join(SCRIPT_DIR, 'argconfig', '__init__.py')
    with open(init_path) as v_file:
        version = re.compile(
            r".*__version__ = '(.*?)'",
            re.S).match(v_file.read()).group(1)

    return version


# TODO:
# - use classifiers, keywords
# - check all of these options
# https://python-packaging.readthedocs.io/en/latest/metadata.html#better-package-metadata

setup(name='argconfig',
      version=get_version(),
      description='Use config files with argparse',
      long_description=readme(),
      url='https://github.com/bbkane/argconfig',
      author='Benjamin Kane',
      author_email='bbk1524@gmail.com',
      license='MIT',
      packages=['argconfig'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      # Do I need this to include the README?
      include_package_data=True,
      zip_safe=False)
