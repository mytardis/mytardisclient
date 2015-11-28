"""
Model class for MyTardis API v1's DataFileResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import mimetypes
import json
import os
import cgi
import hashlib
from datetime import datetime

from mytardisclient.conf import config
from .replica import Replica
from .dataset import Dataset
from .resultset import ResultSet
from .schema import Schema
from .schema import ParameterName
from mytardisclient.utils.exceptions import DoesNotExist


class DataFile(object):
    """
    Model class for MyTardis API v1's DataFileResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, datafile_json):
        self.json = datafile_json
        self.id = datafile_json['id']  # pylint: disable=invalid-name
        self.dataset = datafile_json['dataset']
        self.directory = datafile_json['directory']
        self.filename = datafile_json['filename']
        self.size = datafile_json['size']
        self.md5sum = datafile_json['md5sum']
        self.replicas = []
        for replica_json in datafile_json['replicas']:
            self.replicas.append(Replica(replica_json))
        self.parameter_sets = []
        for datafile_param_set_json in datafile_json['parameter_sets']:
            self.parameter_sets.append(
                DataFileParameterSet(datafile_param_set_json))

    @property
    def verified(self):
        """
        All replicas (DFOs) must be verified and there must be
        at least one replica (DFO).
        """
        if len(self.replicas) == 0:
            return False
        for replica in self.replicas:
            if not replica.verified:
                return False
        return True

    @staticmethod
    @config.region.cache_on_arguments(namespace="DataFile")
    def list(dataset_id=None, directory=None, filename=None,
             limit=None, offset=None, order_by=None):
        """
        Get datafiles I have access to
        """
        # pylint: disable=too-many-arguments
        url = "%s/api/v1/dataset_file/?format=json" % config.url
        if dataset_id:
            url += "&dataset__id=%s" % dataset_id
        if directory:
            url += "&directory=%s" % directory
        if filename:
            url += "&filename=%s" % filename
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)

        if dataset_id or limit or offset:
            filters = dict(dataset_id=dataset_id, limit=limit, offset=offset)
            return ResultSet(DataFile, url, response.json(),
                             **filters)
        else:
            return ResultSet(DataFile, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="DataFile")
    def get(datafile_id):
        """
        Get datafile record with id datafile_id
        """
        url = "%s/api/v1/dataset_file/%s/?format=json" % \
            (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            if response.status_code == 404:
                message = "Datafile with ID %s doesn't exist." % datafile_id
                raise DoesNotExist(message, url, response, DataFile)
            message = response.text
            raise Exception(message)

        datafile_json = response.json()
        return DataFile(datafile_json=datafile_json)

    @staticmethod
    def create(dataset_id, storagebox, file_path):
        """
        Create a datafile record.

        :param dataset_id: The ID of the dataset to create the datafile in.
        :param storagebox: The storage box containing the datafile.
        :param file_path: The local path to the file to be represented in
            the datafile record.

            file_path should be a relative (not absolute) path,
            e.g. dataset1/subdir1/datafile1.txt

            The first directory ('dataset1') in the file_path is the local
            dataset path, which we will create a symlink to in
             ~/.config/mytardisclient/datasets/ which will enable MyTardis
            to verify and ingest the file (see below).  The subdirectory
            ('subdir1') to be recorded in the DataFile record will be
            determined automatically.

        See also: :func:`mytardisclient.models.datafile.DataFile.upload`

        Suppose someone with username james generates a file called
        "results.dat" on a data analysis server called analyzer.example.com
        in the directory ~james/analysis/dataset1/.  User james could grant
        the MyTardis server temporary access to his account on
        analyzer.example.com and then have MyTardis copy the file(s) into
        a more permanent location.

        If james agrees to allow the MyTardis server to do so, it could
        SSHFS-mount james@analyzer.example.com:/home/james/analysis/,
        e.g. at /mnt/sshfs/james-anaylzer/

        Then user james doesn't need to upload results.dat, he just needs to
        tell MyTardis how to access it, and tell MyTardis that it is not yet
        in a permanent location.

        MyTardis's default storage box model generates datafile object
        identifiers which include a dataset description (e.g. 'dataset1')
        and a unique ID, resulting in path like 'dataset1-123/results.dat'
        for the datafile object.  Because user james doesn't want to have
        to create the 'dataset1-123' folder himself, he could entrust the
        MyTardis Client to do it for him.

        The MyTardis administrator can create a storage box for james called
        "james-analyzer" which is of type "receiving", meaning that it is a
        temporary location.  The storage box record (which only needs to be
        accessed by the MyTardis administrator) would include a StorageBoxOption
        with key 'location' and value '/mnt/sshfs/james-analyzer'.

        Once james knows the dataset ID of the dataset he wants to upload to
        (123 in this case), he can create a datafile record as follows:

        mytardis datafile create 123 --storagebox=james-analyzer ~/analysis/dataset1/results.dat

        The file_path argument (set to ~/analysis/dataset1/results.dat)
        specifies the location of 'results.dat' on the analysis server.

        To enable the MyTardis server to access (and verify) the file via
        SSHFS / SFTP, a symbolic link can be created in
        ~james/.mytardisclient/datasets/, named "dataset1-123" pointing to
        the location of 'results.dat', i.e. ~james/analysis/dataset1/.
        """
        # pylint: disable=too-many-locals
        if os.path.isabs(file_path):
            raise Exception("file_path should be relative, not absolute.")
        dataset = Dataset.get(dataset_id)
        file_path_components = file_path.split(os.sep)
        local_dataset_path = file_path_components.pop(0)
        filename = file_path_components.pop(-1)
        if len(file_path_components) > 0:
            directory = os.path.join(*file_path_components)
        else:
            directory = ""
        uri = os.path.join("%s-%s" % (dataset.description, dataset_id),
                           directory, filename)
        dataset_symlink_path = os.path.join(config.datasets_path, uri)
        if not os.path.exists(dataset_symlink_path):
            print "Creating symlink to: %s in " \
                "~/.config/mytardisclient/datasets/ called %s" \
                % (local_dataset_path,
                   "%s-%s" % (dataset.description, dataset_id))
            os.symlink(os.path.abspath(os.path.dirname(file_path)),
                       os.path.join(config.datasets_path,
                                    "%s-%s" % (dataset.description,
                                               dataset_id)))
        md5sum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        replicas = [{
            "url": uri,
            "location": storagebox,
            "protocol": "file",
            "verified": False
        }]
        new_datafile_json = {
            'dataset': "/api/v1/dataset/%s/" % dataset_id,
            'filename': filename,
            'directory': directory or "",
            'md5sum': md5sum,
            'size': str(os.stat(file_path).st_size),
            'mimetype': mimetypes.guess_type(file_path)[0],
            'replicas': replicas,
            'parameter_sets': []
        }
        url = "%s/api/v1/dataset_file/" % config.url
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_datafile_json))
        if response.status_code != 201:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)
        datafile_id = response.headers['location'].split("/")[-2]
        new_datafile = DataFile.get(datafile_id)
        return new_datafile

    @staticmethod
    def download(datafile_id):
        """
        Download datafile with id datafile_id
        """
        url = "%s/api/v1/dataset_file/%s/download/" \
            % (config.url, datafile_id)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.get(url=url, headers=headers, stream=True)
        if response.status_code != 200:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)
        try:
            _, params = cgi.parse_header(
                response.headers.get('Content-Disposition', ''))
            filename = params['filename']
        except KeyError:
            print "response.headers: %s" % response.headers
            raise
        fileobj = open(filename, 'wb')
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fileobj.write(chunk)
        print "Downloaded: %s" % filename

    @staticmethod
    def upload(dataset_id, file_path):
        """
        Upload datafile to dataset with ID dataset_id,
        using HTTP POST.
        """
        url = "%s/api/v1/dataset_file/" % config.url
        created_time = datetime.fromtimestamp(
            os.stat(file_path).st_ctime).isoformat()
        md5sum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        file_path_components = file_path.split(os.sep)
        _ = file_path_components.pop(0)  # local_dataset_path
        filename = file_path_components.pop(-1)
        if len(file_path_components) > 0:
            directory = os.path.join(*file_path_components)
        else:
            directory = ""
        file_data = {"dataset": "/api/v1/dataset/%s/" % dataset_id,
                     "filename": filename,
                     "directory": directory,
                     "md5sum": md5sum,
                     "size": str(os.stat(file_path).st_size),
                     "mimetype": mimetypes.guess_type(file_path)[0],
                     "created_time": created_time}
        file_obj = open(file_path, 'rb')
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.post(url, headers=headers,
                                 data={"json_data": json.dumps(file_data)},
                                 files={'attached_file': file_obj})
        file_obj.close()
        if response.status_code != 201:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)
        if directory:
            print "Uploaded: %s/%s" % (directory, file_path)
        else:
            print "Uploaded: %s" % file_path

    @staticmethod
    def update(datafile_id, md5sum):
        """
        Update a datafile record.

        Only the md5sum field can be updated at present.
        For a large file, its upload can commence before
        the local MD5 sum calculation is complete, i.e.
        the datafile record can be initially created with
        a bogus checksum which is later corrected.
        """
        updated_fields_json = {'md5sum': md5sum}
        url = "%s/api/v1/dataset_file/%s/" % \
            (config.url, datafile_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)
        datafile_json = response.json()
        return DataFile(datafile_json)

    @staticmethod
    def verify(datafile_id):
        """
        Ask MyTardis to verify a datafile with id datafile_id
        """
        url = "%s/api/v1/dataset_file/%s/verify/" \
            % (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)
        print "Requested verification of datafile ID %s." % datafile_id


class DataFileParameterSet(object):
    """
    Model class for MyTardis API v1's DataFileParameterSetResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, datafile_paramset_json):
        self.json = datafile_paramset_json
        self.id = datafile_paramset_json['id']  # pylint: disable=invalid-name
        self.datafile = datafile_paramset_json['datafile']
        self.schema = Schema(datafile_paramset_json['schema'])
        self.parameters = []
        for datafile_param_json in datafile_paramset_json['parameters']:
            self.parameters.append(DataFileParameter(datafile_param_json))

    @staticmethod
    @config.region.cache_on_arguments(namespace="DataFileParameterSet")
    def list(datafile_id):
        """
        List datafile parameter sets associated with datafile ID
        datafile_id.
        """
        url = "%s/api/v1/datafileparameterset/?format=json" % config.url
        url += "&datafiles__id=%s" % datafile_id
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "HTTP %s" % response.status_code
            print "URL: %s" % url
            message = response.text
            raise Exception(message)

        filters = dict(datafile_id=datafile_id)
        return ResultSet(DataFileParameterSet, url, response.json(), **filters)


class DataFileParameter(object):
    """
    Model class for MyTardis API v1's DataFileParameterResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, datafile_param_json):
        self.json = datafile_param_json
        self.id = datafile_param_json['id']  # pylint: disable=invalid-name
        self.name = ParameterName.get(datafile_param_json['name'].split('/')[-2])
        self.string_value = datafile_param_json['string_value']
        self.numerical_value = datafile_param_json['numerical_value']
        self.datetime_value = datafile_param_json['datetime_value']
        self.link_id = datafile_param_json['link_id']
        self.value = datafile_param_json['value']

    @staticmethod
    @config.region.cache_on_arguments(namespace="DataFileParameter")
    def list(datafile_param_set):
        """
        List datafile parameter records in parameter set.
        """
        pass
