import argparse
import json
import sys
from typing import List


class InfoSource:

    # This is just to pass the parser into the class
    # without having to do it in the __init__ method,
    # so people who make this class don't have to pass
    # the parser every time
    def set_info(self, parser, parsed_passed_args):
        self.parser = parser
        self.parsed_passed_args = parsed_passed_args


class ScriptDefaults(InfoSource):

    # this needs to return a dict of options
    def parse_args(self, *args, **kwargs):
        # parse an empty list to get the defaults
        return vars(self.parser.parse_args([]))


class PassedArgs(InfoSource):

    def parse_args(self, *args, **kwargs):

        defaults = vars(self.parser.parse_args([]))

        # Only keep the args that aren't the default
        # so not everything overwrites
        passed_args = {key: value for (key, value) in self.parsed_passed_args.items()
                       if (key in defaults and defaults[key] != value)}

        return passed_args


class PassedJSONConfig(InfoSource):

    def parse_args(self, *args, **kwargs):

        config_path = self.parsed_passed_args.pop('config', None)
        if config_path:
            with open(config_path, 'r') as config_file:
                configargs = json.load(config_file)
        else:
            configargs = dict()
        return configargs


# Add a config subparser to the parser passed in
# add a --config option that overwrites the defaults
# and is overwritten by the passed in arguments
class ArgumentConfig:
    def __init__(self, parser: argparse.ArgumentParser,
                 info_sources: List[InfoSource]):
        self.parser = parser

        self.info_sources = info_sources

        self.parser.add_argument('--config', '-c',
                                 nargs='?',
                                 metavar='FILENAME')

        self.parser.add_argument('--write_config', '-wc',
                                 nargs='?',
                                 metavar='FILENAME',
                                 const='stdout')

        self.parser.add_argument('--list_overrides',
                                 action='store_true',
                                 help='List all options from all parsers'
                                      '. Later options override previous ones')

    def parse_args(self, *args, **kwargs):

        # parse the passed args. This is needed so I can get a passed config
        parsed_passed_args = vars(self.parser.parse_args(*args, *kwargs))

        options = {}
        overrides = []
        for info_source in self.info_sources:
            info_source.set_info(self.parser, parsed_passed_args)
            info_source_args = info_source.parse_args()
            overrides.append(info_source_args)
            options.update(info_source_args)

        # remove the config options from options. They're not needed any more
        # and we don't want them serialized
        options.pop('config', None)
        options.pop('write_config', None)
        options.pop('list_overrides')

        # list all the overrides if necessary
        if parsed_passed_args['list_overrides']:
            import pprint
            for override in overrides:
                pprint.pprint(override)
            sys.exit(0)

        # print the options (to file) if needed
        config_dst = parsed_passed_args.pop('write_config', None)
        if config_dst:
            print(json.dumps(options, sort_keys=True, indent=4))
            if config_dst != 'stdout':
                with open(config_dst, 'w', encoding='utf-8') as config_file:
                    print(json.dumps(options, sort_keys=True, indent=4), file=config_file)
                    print('Current options saved to: %r' % config_dst)
            sys.exit(0)

        return argparse.Namespace(**options)
