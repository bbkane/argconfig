import argparse
import json
import sys


class Parser:

    # This is just to pass the parser into the class
    # without having to do it in the __init__ method,
    # so people who make this class don't have to pass
    # the parser every time
    def set_info(self, parser, parsed_passed_args):
        self.parser = parser
        self.parsed_passed_args = parsed_passed_args


class ScriptDefaults(Parser):

    # this needs to return a dict of options
    def parse_args(self, *args, **kwargs):
        # parse an empty list to get the defaults
        return vars(self.parser.parse_args([]))


class PassedArgs(Parser):

    def parse_args(self, *args, **kwargs):

        # TODO: is there a cleaner way of doing this?
        # I'm parsing the arguments to just to get the changed
        # ones
        defaults = vars(self.parser.parse_args([]))

        # Only keep the args that aren't the default
        # so not everything overwrites
        passed_args = {key: value for (key, value) in self.parsed_passed_args.items()
                       if (key in defaults and defaults[key] != value)}

        return passed_args


# TODO: is this a confusing name?
class PassedJSONConfigArgs(Parser):

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
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        # TODO: don't hardcode
        self.parsers = [ScriptDefaults(), PassedJSONConfigArgs(), PassedArgs()]

        self.parser.add_argument('--config', '-c',
                                 nargs='?',
                                 metavar='FILENAME')

        # TODO: put this in subparser?
        self.parser.add_argument('--write_config', '-wc',
                                 nargs='?',
                                 metavar='FILENAME',
                                 const='stdout')

    def parse_args(self, *args, **kwargs):

        # parse the passed args. This is needed so I can get a passed config
        parsed_passed_args = vars(self.parser.parse_args(*args, *kwargs))

        options = {}
        for parser in self.parsers:
            parser.set_info(self.parser, parsed_passed_args)
            options.update(parser.parse_args())

        # remove the config options from options. They're not needed any more
        # and we don't want them serialized
        options.pop('config', None)
        options.pop('write_config', None)

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
