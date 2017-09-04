import argparse
import json
import sys
from typing import List, Dict


class InfoSource:

    # This is just to pass the parser into the class
    # without having to do it in the __init__ method,
    # so people who make this class don't have to pass
    # the parser every time
    def set_info(self, parser, parsed_passed_args, parsed_default_args, config_path):
        self.parser = parser
        self.parsed_passed_args = parsed_passed_args
        self.parsed_default_args = parsed_default_args
        # Could be None
        self.config_path = config_path

    def parse_args(self) -> Dict:
        pass


class ScriptDefaults(InfoSource):

    # this needs to return a dict of options
    def parse_args(self, *args, **kwargs):
        # parse an empty list to get the defaults
        return self.parsed_default_args


class PassedArgs(InfoSource):

    def parse_args(self):

        defaults = self.parsed_default_args

        # Only keep the args that aren't the default
        # so not everything overwrites
        passed_args = {key: value for (key, value) in self.parsed_passed_args.items()
                       if (key in defaults and defaults[key] != value)}

        return passed_args

# Notes on config specialization:
# How I'm doing this now is:
# - base class ( named <filetype>Source ) with parsing file method (inherits
#   from InfoSource so it has access to set_info stuff)
# - derived <filetype>Config and Passed<filetype>Config classes that specialize __init__ so the user
# gets pretty constructors


class JSONSource(InfoSource):
    """
    Helper class that's specialized below
    """

    def _parse_args(self, path):
        if path:
            with open(path, 'r') as config_file:
                configargs = json.load(config_file)
        else:
            configargs = {}
        return configargs


class JSONConfig(JSONSource):

    def __init__(self, path):
        self.path = path

    def parse_args(self):
        return self._parse_args(self.path)


class PassedJSONConfig(JSONSource):

    def parse_args(self):
        return self._parse_args(self.config_path)


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

        # remove the config options from parsed_passed_args
        # they're special to us, and parsers don't need to know about them
        ppa_config = parsed_passed_args.pop('config', None)
        ppa_write_config = parsed_passed_args.pop('write_config', None)
        ppa_list_overrides = parsed_passed_args.pop('list_overrides', None)

        # do the same thing with the default args
        # We don't want them carried on to the info sources
        parsed_default_args = vars(self.parser.parse_args([]))
        parsed_default_args.pop('config', None)
        parsed_default_args.pop('write_config', None)
        parsed_default_args.pop('list_overrides', None)

        options = {}
        overrides = []
        for info_source in self.info_sources:
            info_source.set_info(self.parser, parsed_passed_args, parsed_default_args,
                                 ppa_config)
            info_source_args = info_source.parse_args()
            overrides.append(info_source_args)
            options.update(info_source_args)

        # list all the overrides if necessary
        if ppa_list_overrides:
            import pprint
            for override in overrides:
                pprint.pprint(override)
            sys.exit(0)

        # print the options (to file) if needed
        config_dst = ppa_write_config
        if config_dst:
            print(json.dumps(options, sort_keys=True, indent=4))
            if config_dst != 'stdout':
                with open(config_dst, 'w', encoding='utf-8') as config_file:
                    print(json.dumps(options, sort_keys=True, indent=4), file=config_file)
                    print('Current options saved to: %r' % config_dst)
            sys.exit(0)

        return argparse.Namespace(**options)
