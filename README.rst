argconfig
=========

*Not Ready For Usage Yet*
-------------------------

This module wraps ``argparse.ArgumentParser`` so arguments passed to it
can be overwritten in the following order:

-  script default configuration - overwritten by any of the following
-  system config
-  user config
-  environmental variables (with an optional prefix)
-  explicitly passed config
-  explicitly passed arguments - never overwritten

Sample usage:
-------------

-  in file ``addem.py``:

TODO: add actual config stuff here...

.. code:: python

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--integers', metavar='N', type=int, nargs='+',
                        default=[1, 2, 3],
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const='sum', default='max',
                        help='sum the integers (default: find the max)')

    options = ArgumentConfig(parser)

    o = options.parse_args()

    print(o)

-  in file ``config.json``:

.. code:: json

    {
        "accumulate": "max",
        "integers": [
            1,
            2,
            3
        ]
    }

Then call it like so:

.. code:: bash

    python addem.py -c config.json --sum

Notes
-----

This isn't 100% compatible with ``argparse``. In general, your arguments
must resolve to JSON serializable types (``int``, ``string``, etc.). In
particular, you can't assign a function to the ``default`` or ``const``
arguments in your parser. As I like to dispatch actions from a central
main function anyway, this hasn't bothered me.

I'm using reStructuredText instead of Markdown so I can upload this as the PyPy package index more easily.

Convert between extensions (in this case ``md`` and ``rst``) with ``pandoc -o <name>.rst <name.md``

I'm following the guide at `the python-packaging readthedocs <https://python-packaging.readthedocs.io/en/latest/index.html>`__.

That's pretty much done. Now I'm using the docs at `pytest <https://docs.pytest.org/en/latest/goodpractices.html#goodpractices>`__ to use py.test with this.

Install and Test
----------------

.. code:: bash

    cd ~/Git/
    git clone https://github.com/bbkane/argconfig.git
    cd argconfig
    conda create --name argconfig python=3
    source activate argconfig
    pip install -e .
    python setup.py test
    # run with pdb for debugging
    python setup.py test --addopts --pdb
    # run tests on save (requires entr)
    git ls-files | entr python setup.py test

TODO:
-----

- config backends:

  - configobj
  - env
  - pyyaml (requires an optional dependency)
  - api?

- comments in the JSON
- write parsers in other things than JSON
- change write_config to output other things than JSON
- make --list-overrides not look so ugly (add things to specify what is overriding what)
- add docs
- put library commands in subparser?
