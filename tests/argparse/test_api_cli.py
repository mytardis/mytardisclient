"""
tests/argparse/test_api_cli.py
"""
import sys

from mtclient.argparser import ArgParser


def test_api_argparse():
    """
    Test command-line interface for querying API endpoints
    """
    sys_argv = sys.argv
    sys.argv = ['mytardis', 'api', 'list']
    args = ArgParser().get_args()
    assert args.model == 'api'
    assert args.command == 'list'
    assert not args.json
    assert not args.verbose

    sys.argv = ['mytardis', 'api', 'get', 'dataset', '--json']
    args = ArgParser().get_args()
    assert args.model == 'api'
    assert args.command == 'get'
    assert args.json
    assert not args.verbose

    sys.argv = sys_argv
