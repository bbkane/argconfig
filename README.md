# argconfig

This module wraps `argparse.ArgumentParser` so arguments passed to it can be overwritten in the following order:

- system config - overwritten by any of the following
- user config
- environmental variables (with an optional prefix)
- explicitly passed config
- explicitly passed arguments - never overwritten

Sample usage:

```python
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
```

Then call it like so:

```

```
