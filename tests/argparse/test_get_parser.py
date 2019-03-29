"""
tests/argparse/test_get_parser.py
"""
from mtclient.argparser import get_parser


def test_get_parser():
    """
    Test get_parser() method used by sphinx-argparse
    """
    parser = get_parser()
    assert parser.description == "Command-line interface for MyTardis REST API."
