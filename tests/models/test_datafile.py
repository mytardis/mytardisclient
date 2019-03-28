"""
test_datafile.py

Tests for functionality to query the DataFile model via
the MyTardis REST API's datafile resource
"""
import json
import tempfile

import pytest
import requests_mock

from mtclient.conf import config
from mtclient.models.datafile import DataFile


def test_datafile_list():
    """
    Test listing datafile records exposed in a MyTardis REST API
    """
    mock_datafile_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [{
            "id": 1,
            "created_time": "2016-11-10T13:50:25.258483",
            "dataset": "/api/v1/dataset/1/",
            "directory": "subdir",
            "filename": "testfile1.txt",
            "md5sum": "bogus",
            "mimetype": "text/plain",
            "modification_time": None,
            "parameter_sets": [
            ],
            "replicas": [
                {
                    "datafile": "/api/v1/dataset_file/1/",
                    "id": 1,
                    "location": "local box at /home/mytardis/var/local",
                    "resource_uri": "/api/v1/replica/1/",
                    "uri": "subdir/testfile1.txt",
                    "verified": True
                }
            ],
            "resource_uri": "/api/v1/dataset_file/1/",
            "size": 32,
        }]
    }
    mock_list_response = json.dumps(mock_datafile_list)
    with requests_mock.Mocker() as mocker:
        list_datafiles_url = "%s/api/v1/dataset_file/?format=json&dataset__id=1" % config.url
        mocker.get(list_datafiles_url, text=mock_list_response)
        datafiles = DataFile.list(dataset_id=1)
        assert datafiles.response_dict == mock_datafile_list


def test_datafile_get():
    """
    Test getting a datafile record by ID
    """
    mock_datafile = {
        "id": 1,
        "created_time": "2016-11-10T13:50:25.258483",
        "dataset": "/api/v1/dataset/1/",
        "directory": "subdir",
        "filename": "testfile1.txt",
        "md5sum": "bogus",
        "mimetype": "text/plain",
        "modification_time": None,
        "parameter_sets": [
        ],
        "replicas": [
            {
                "datafile": "/api/v1/dataset_file/1/",
                "id": 1,
                "location": "local box at /home/mytardis/var/local",
                "resource_uri": "/api/v1/replica/1/",
                "uri": "subdir/testfile1.txt",
                "verified": True
            }
        ],
        "resource_uri": "/api/v1/dataset_file/1/",
        "size": 32,
    }
    mock_get_response = json.dumps(mock_datafile)
    with requests_mock.Mocker() as mocker:
        get_datafile_url = "%s/api/v1/dataset_file/1/?format=json" % config.url
        mocker.get(get_datafile_url, text=mock_get_response)
        datafile = DataFile.objects.get(id=1)
        assert datafile.response_dict == mock_datafile
        assert str(datafile) == "<DataFile: subdir/testfile1.txt>"
        with pytest.raises(NotImplementedError) as err:
            DataFile.objects.get(invalid_key="value")
            assert str(err) == (
                "Only the id keyword argument is supported for DataFile get "
                "at this stage.")


def test_datafile_create():
    """
    Test creating a datafile record
    """
    # DataFile.create_datafile(...) will look up the Dataset specified by
    # its dataset_id argument, so we need to mock the response for this
    # Dataset lookup:
    mock_dataset = {
        "created_time": None,
        "description": "dataset description",
        "directory": None,
        "experiments": [
            "/api/v1/experiment/1/"
        ],
        "id": 1,
        "immutable": False,
        "instrument": None,
        "modified_time": None,
        "parameter_sets": [],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_ds_get_response = json.dumps(mock_dataset)

    # DataFile.create_datafile(...) will check whether a DataFile already
    # exists with this dataset ID, filename and directory, so we need to
    # mock the response for this DataFile lookup:
    mock_datafile_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 0
        },
        "objects": [
        ]
    }
    mock_df_list_response = json.dumps(mock_datafile_list)

    # The MyTardis API's DataFile creation endpoint returns the newly
    # created DataFile ID in the response header, but DataFile.create_datafile
    # needs to query the API again to get the full details of the newly created
    # DataFile record, so we'll mock this DataFile lookup:
    mock_new_datafile = {
        "id": 1,
        "created_time": "2016-11-10T13:50:25.258483",
        "dataset": "/api/v1/dataset/1/",
        "directory": "subdir",
        "filename": "testfile1.txt",
        "md5sum": "bogus",
        "mimetype": "text/plain",
        "modification_time": None,
        "parameter_sets": [
        ],
        "replicas": [
            {
                "datafile": "/api/v1/dataset_file/1/",
                "id": 1,
                "location": "local box at /home/mytardis/var/local",
                "resource_uri": "/api/v1/replica/1/",
                "uri": "subdir/testfile1.txt",
                "verified": True
            }
        ],
        "resource_uri": "/api/v1/dataset_file/1/",
        "size": 32,
    }
    mock_new_df_response = json.dumps(mock_new_datafile)
    with requests_mock.Mocker() as mocker:
        get_dataset_url = "%s/api/v1/dataset/1/?format=json" % config.url
        mocker.get(get_dataset_url, text=mock_ds_get_response)
        df_list_url = ("%s/api/v1/dataset_file/?format=json"
                       "&filename=testfile.txt"
                       "&directory=subdir" % config.url)
        mocker.get(df_list_url, text=mock_df_list_response)
        post_datafile_url = "%s/api/v1/dataset_file/" % config.url
        mocker.post(post_datafile_url,
                    headers=dict(location="/api/v1/dataset_file/1/"))
        get_new_df_url = "%s/api/v1/dataset_file/1/?format=json" % config.url
        mocker.get(get_new_df_url, text=mock_new_df_response)
        datafile = DataFile.create_datafile(
            dataset_id=1,
            storagebox="local box at /home/mytardis/var/local",
            dataset_path="/path/to/dataset1",
            file_path="/path/to/dataset1/subdir/testfile.txt",
            check_local_paths=False,
            create_dataset_symlink=False,
            size=32,
            md5sum="bogus")
        assert datafile.response_dict == mock_new_datafile


def test_md5_sum():
    """
    Test calculating the MD5 sum of a datafile
    """
    import os
    import sys

    from mtclient.models.datafile import md5_sum

    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile_name = tmpfile.name

    with open(tmpfile_name, 'w') as tmpfile:
        tmpfile.write("Hello, world!\n")

    assert md5_sum(tmpfile_name) == "746308829575e17c3331bbcb00c0898b"

    try:
        os.remove(tmpfile_name)
    except IOError as err:
        sys.stderr.write("%s\n" % err)
