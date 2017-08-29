from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='argconfig',
      version='0.0.1',
      description='Use config files with argparse',
      long_description=readme(),
      url='https://github.com/bbkane/argconfig',
      author='Benjamin Kane',
      author_email='bbk1524@gmail.com',
      license='MIT',
      packages=['argconfig'],
      zip_safe=False)
