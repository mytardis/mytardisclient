"""
Test for command-line yes/no confirmation
"""
import sys
from io import StringIO

import pytest

from mtclient.utils.confirmation import query_yes_no


def test_query_yes_no(capfd):
    """
    Test for command-line yes/no confirmation
    """
    sys_stdin = sys.stdin

    sys.stdin = StringIO("y\n")
    assert query_yes_no("Question?")
    out, _ = capfd.readouterr()
    assert out == "Question? [y/n] "

    sys.stdin = StringIO("n\n")
    assert not query_yes_no("Question?")
    out, _ = capfd.readouterr()
    assert out == "Question? [y/n] "

    sys.stdin = StringIO("\n")
    assert query_yes_no("Question?", default="yes")
    out, _ = capfd.readouterr()
    assert out == "Question? [Y/n] "

    sys.stdin = StringIO("\n")
    assert not query_yes_no("Question?", default="no")
    out, _ = capfd.readouterr()
    assert out == "Question? [y/N] "

    with pytest.raises(ValueError) as err:
        query_yes_no("Question?", default="invalid_default")
        assert str(err) == "invalid default answer: 'invalid_default'"

    sys.stdin = StringIO("invalid\ny\n")
    assert query_yes_no("Question?")
    out, _ = capfd.readouterr()
    assert out == (
        "Question? [y/n] "
        "Please respond with 'yes' or 'no' "
        "(or 'y' or 'n').\n"
        "Question? [y/n] ")

    sys.stdin = sys_stdin
