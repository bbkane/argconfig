import argparse
import json
import os
import sys


# Add a config subparser to the parser passed in
# add a --config option that overwrites the defaults
# and is overwritten by the passed in arguments
class ArgumentConfig:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument('--configargs', '-c',
                                 nargs='?',
                                 metavar='FILENAME')

        # TODO: put this in subparser
        self.parser.add_argument('--write_config', '-wc',
                                 nargs='?',
                                 metavar='FILENAME',
                                 const='stdout')

        # parse an empty list to get the defaults
        self.defaults = vars(self.parser.parse_args([]))

        # TODO: add config subparser here

    def parse_args(self, *args, **kwargs):

        passed_args = vars(self.parser.parse_args(*args, **kwargs))

        # Only keep the args that aren't the default
        passed_args = {key: value for (key, value) in passed_args.items()
                       if (key in self.defaults and self.defaults[key] != value)}

        # TODO: deal with any config subparser stuff we've added

        if passed_args.get('configargs', None):
            config_path = os.path.expanduser(passed_args['configargs'])
            with open(config_path, 'r') as config_file:
                configargs = json.load(config_file)
        else:
            configargs = dict()

        # if we need to write the config, get the path
        if 'write_config' in passed_args:
            config_dst = passed_args.pop('write_config')
        else:
            config_dst = None

        # override defaults with config with passed args
        options = {**self.defaults, **configargs, **passed_args}

        # remove the config options from options. They're not needed any more
        # and we don't want them serialized
        options.pop('configargs', None)
        options.pop('write_config', None)

        # print the options (to file) if needed
        if config_dst:
            print(json.dumps(options, sort_keys=True, indent=4))
            if config_dst != 'stdout':
                with open(config_dst, 'w', encoding='utf-8') as config_file:
                    print(json.dumps(options, sort_keys=True, indent=4), file=config_file)
            sys.exit(0)

        return argparse.Namespace(**options)


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

# defaults = parser.parse_args([])
# print(defaults)

# args = parser.parse_args()
# print(args)
# print(args.accumulate(args.integers))
