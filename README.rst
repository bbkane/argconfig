argconfig
=========

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

TODO:
-----

-  multiple config backends (not just JSON)
-  comments in the JSON
