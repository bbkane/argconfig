import argparse
import argconfig
import json

import pytest

# Notes:
# Run this with `pytest --pdb` at the root dir and you'll get pdb on assertion
# use `@pytest.mark.skip(reason="the reason")` to skip tests


# https://docs.pytest.org/en/latest/tmpdir.html#the-tmpdir-factory-fixture
# By using a fixture and an arg named tmpdir_factory, I can create a file
# that will be erased at the end of the session.
# use the new config file by making 'json_config_file' an arg to another config
@pytest.fixture(scope='session')
def json_config_file(tmpdir_factory):
    config = {'json_default': 'overwritten_by_json_config'}
    pytest_file = tmpdir_factory.mktemp('config').join('config.json')
    with open(str(pytest_file), 'w') as f:
        json.dump(config, f, sort_keys=True, indent=None)

    return pytest_file


def build_parser():
    parser = argparse.ArgumentParser(description='Testing it')
    parser.add_argument('--script_default', default='not_overwritten')
    parser.add_argument('--arg_default', default='not_overwritten')
    parser.add_argument('--json_default', default='not_overwritten')

    return parser


def test_argconfig_overwrite_all_with_args(json_config_file):
    parser = build_parser()

    options = argconfig.ArgumentConfig(parser)

    parsed_args = options.parse_args(['--arg_default', 'overwritten_by_arg',
                                      '--script_default', 'overwritten_by_arg',
                                      '--json_default', 'overwritten_by_arg',
                                      '--config', str(json_config_file)])
    parsed_args_dict = vars(parsed_args)

    answers = dict(arg_default='overwritten_by_arg',
                   script_default='overwritten_by_arg',
                   json_default='overwritten_by_arg')

    assert parsed_args_dict == answers


# Right now this tests a passed arg, a script default, and a json-passed config
def test_argconfig(json_config_file):

    parser = build_parser()

    options = argconfig.ArgumentConfig(parser)

    parsed_args = options.parse_args(['--arg_default', 'overwritten_by_arg',
                                      '--config', str(json_config_file)])
    parsed_args_dict = vars(parsed_args)

    answers = dict(arg_default='overwritten_by_arg',
                   script_default='not_overwritten',
                   json_default='overwritten_by_json_config')

    assert parsed_args_dict == answers
