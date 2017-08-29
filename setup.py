from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

# TODO:
# - use classifiers, keywords
# - check all of these options
# add __version__ attr

setup(name='argconfig',
      version='0.0.1',
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
