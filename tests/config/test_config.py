"""
tests/config/test_config.py
"""
import json
import os
import sys
import tempfile
import textwrap

import pytest

from mtclient.conf import config
from mtclient.utils.exceptions import InvalidConfig


def test_validation():
    """
    Test configuration validation
    """
    assert config.validate()

    config_url = config.url
    config.url = ""
    with pytest.raises(InvalidConfig) as err:
        config.validate()
    config.url = config_url
    assert err.type == InvalidConfig
    assert "MyTardis URL is missing from config" in str(err)

    config_url = config.url
    config.url = "invalid://example.com"
    with pytest.raises(InvalidConfig) as err:
        config.validate()
    config.url = config_url
    assert err.type == InvalidConfig
    assert "Invalid MyTardis URL found in config" in str(err)

    config_username = config.username
    config.username = ""
    with pytest.raises(InvalidConfig) as err:
        config.validate()
    config.username = config_username
    assert err.type == InvalidConfig
    assert "MyTardis username is missing from config" in str(err)

    config_apikey = config.apikey
    config.apikey = ""
    with pytest.raises(InvalidConfig) as err:
        config.validate()
    config.apikey = config_apikey
    assert err.type == InvalidConfig
    assert "MyTardis API key is missing from config" in str(err)

def test_string_repr():
    """
    Test string representation
    """
    config_dict = config.__dict__
    # datasets_path is a property method, whose value
    # gets displayed in the string represetnation:
    config_dict["datasets_path"] = config.datasets_path
    assert json.loads(str(config)) == config_dict

def test_save():
    """
    Test saving config to disk
    """
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile_path = tmpfile.name

    config.save(tmpfile_path)

    with open(tmpfile_path, 'r') as config_file:
        config_file_content = config_file.read()

    expected = textwrap.dedent("""
    [mytardisclient]
    url = %s
    username = %s
    apikey = %s
    """ % (config.url, config.username, config.apikey))

    assert config_file_content.strip() == expected.strip()
    try:
        os.remove(tmpfile_path)
    except IOError as err:
        sys.stderr.write("%s\n" % err)
