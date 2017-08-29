import argparse
import argconfig


# TODO: replace this with pytest
def test_argconfig():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--integers', metavar='N', type=int, nargs='+',
                        default=[1, 2, 3],
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const='sum', default='max',
                        help='sum the integers (default: find the max)')

    options = argconfig.ArgumentConfig(parser)

    o = options.parse_args()

    # TODO: get a better test
    assert o is not None
