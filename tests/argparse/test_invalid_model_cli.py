"""
tests/argparse/test_invalid_model_cli.py
"""
import sys
import textwrap

import pytest

from mtclient.argparser import ArgParser


def test_invalid_model_argparse(capfd):
    """
    Test command-line interface with invalid model name
    """
    sys_argv = sys.argv
    sys.argv = ['mytardis', 'invalid_model', 'list']

    with pytest.raises(SystemExit) as err:
        ArgParser().get_args()
    assert err.value.code == 2

    expected = textwrap.dedent("""
         usage: mytardis [-h] [--verbose] [--version]
                         {api,config,version,facility,instrument,experiment,dataset,datafile,storagebox,schema}
                         ...
         mytardis: error: argument model: invalid choice: 'invalid_model' (choose from 'api', 'config', 'version', 'facility', 'instrument', 'experiment', 'dataset', 'datafile', 'storagebox', 'schema')
    """)
    _, err = capfd.readouterr()
    assert err.strip() == expected.strip()

    sys.argv = sys_argv
