"""
Model class for MyTardis API v1's DataFileResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""
from __future__ import print_function

import mimetypes
import json
import os
import cgi
import hashlib
import urllib2
import logging
from datetime import datetime

import requests

from mytardisclient.conf import config
from .replica import Replica
from .dataset import Dataset
from .resultset import ResultSet
from .schema import Schema
from .schema import ParameterName
from mytardisclient.utils.exceptions import DoesNotExist
from mytardisclient.utils.exceptions import DuplicateKey

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

def md5_sum(file_path, blocksize=65536):
    """
    Calculate MD5 checksum without reading the whole file into memory.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as datafile:
        buf = datafile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = datafile.read(blocksize)
        return hasher.hexdigest()


class DataFile(object):
    """
    Model class for MyTardis API v1's DataFileResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, datafile_json, include_metadata=True):
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
        if include_metadata:
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
    def list(dataset_id=None, directory=None, filename=None, filters=None,
             limit=None, offset=None, order_by=None):
        """
        Retrieve a list of datafiles.

        :param dataset_id: The ID of a dataset to retrieve datafiles from.
        :param directory: The subdirectory within the dataset.
        :param filename: The datafile's name.
        :param filters: Filters, e.g. "filename=file1.txt"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`DataFile` records.
        """
        # pylint: disable=too-many-arguments
        url = "%s/api/v1/dataset_file/?format=json" % config.url
        if dataset_id:
            url += "&dataset__id=%s" % dataset_id
        if directory:
            url += "&directory=%s" % directory
        if filename:
            url += "&filename=%s" % filename
        if filters:
            filter_components = filters.split('&')
            for filter_component in filter_components:
                field, value = filter_component.split('=')
                url += "&%s=%s" % (field, urllib2.quote(value))
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        return ResultSet(DataFile, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="DataFile")
    def get(datafile_id, include_metadata=True):
        """
        Retrieve DataFile record with id datafile_id

        :param datafile_id: The ID of a datafile to retrieve.

        :return: A :class:`DataFile` record.
        """
        url = "%s/api/v1/dataset_file/%s/?format=json" % \
            (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            if response.status_code == 404:
                message = "Datafile with ID %s doesn't exist." % datafile_id
                raise DoesNotExist(message, url, response, DataFile)
            message = response.text
            raise Exception(message)

        datafile_json = response.json()
        return DataFile(datafile_json=datafile_json,
                        include_metadata=include_metadata)

    @staticmethod
    def create(dataset_id, storagebox, dataset_path, path):
        """
        Create one or more DataFile records, depending on whether the
        supplied path is a single file or a directory.

        :param dataset_id: The ID of the dataset to create the datafile
            record(s) in.
        :param storagebox: The storage box containing the datafile(s).
        :param dataset_path:
            Only required if the supplied path to the datafile(s) is absolute
            (not relative).  If a relative path is supplied, then dataset_path
            is automatically set to the first component of the relative path.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file.
        :param path: The path to a file to be represented in the DataFile
            record or to a directory containing the files to create records
            for.
            If the path is a relative (not absolute) path,
            e.g. 'dataset1/subdir1/datafile1.txt', then the first directory
            ('dataset1') in the path is assumed to be the local dataset path.
            The MyTardis Client will create a symlink to the local dataset path
            in ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file.
            If the path is an absolute path, e.g.
            '/home/james/dataset1/subdir1/datafile1.txt', then the dataset_path
            argument must be used to specified the dataset path, e.g.
            '/home/james/dataset1'.
        """
        if not dataset_path and os.path.isabs(path):
            raise Exception("Either supply dataset_path or supply a relative "
                            "path to the datafile(s).")
        elif not os.path.exists(path):
            raise Exception("The path doesn't exist: %s" % path)
        if os.path.isdir(path):
            return DataFile.create_datafiles(dataset_id, storagebox,
                                             dataset_path, path)
        else:
            return DataFile.create_datafile(dataset_id, storagebox,
                                            dataset_path, path)

    @staticmethod
    def create_datafiles(dataset_id, storagebox, dataset_path, dir_path):
        """
        Create a DataFile record for each file within the dir_path directory.

        :param dataset_id: The ID of the dataset to create the datafile
            record(s) in.
        :param storagebox: The storage box containing the datafile(s).
        :param dataset_path:
            Only required if the supplied dir_path is absolute (not relative).
            If a relative path is supplied, then dataset_path
            is automatically set to the first component of the relative path.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file.
        :param dir_path: The path to a directory containing file(s) to
            create DataFile records for.  If the dir_path is relative (not
            absolute) path, e.g. 'dataset1/subdir1', then the MyTardis Client
            will assume that the first component of the path (e.g. 'dataset1/')
            is the local dataset path, and create a symlink to this path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/
            which will enable MyTardis to verify and ingest its file(s).
            If dir_path is an absolute path, e.g.
            '/home/james/dataset1/subdir1/', then the dataset_path
            argument must be used to specified the dataset path, e.g.
            '/home/james/dataset1'.
        """
        num_datafiles_created = 0

        def log_error(err):
            """
            Log an error if os.listdir(...) fails during os.walk(...)
            """
            logger.error(str(err))

        for root, _, files in os.walk(dir_path, onerror=log_error):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    DataFile.create_datafile(dataset_id, storagebox,
                                             dataset_path, file_path,
                                             return_new_datafile=False)
                    num_datafiles_created += 1
                except DuplicateKey:
                    logger.warning("A DataFile record already exists for %s",
                                   file_path)
        return num_datafiles_created

    @staticmethod
    def create_datafile(dataset_id, storagebox, dataset_path, file_path,
                        return_new_datafile=True):
        """
        Create a DataFile record.

        :param dataset_id: The ID of the dataset to create the datafile in.
        :param storagebox: The storage box containing the datafile.
        :param dataset_path:
            Only required if the supplied path to the datafile is absolute
            (not relative).  If a relative file_path is specified, and
            dataset_path is not specified, then  dataset_path is
            automatically set to the first component of the file_path.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file.
        :param file_path: The local path to the file to be represented in
            the DataFile record.  If file_path is a relative (not absolute)
            path, e.g. 'dataset1/subdir1/datafile1.txt', then the first
            directory ('dataset1') in the file_path is assumed to be the local
            dataset path, which we will create a symlink to in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/.  This  will
            enable MyTardis to verify and ingest the file.  The subdirectory
            ('subdir1') to be recorded in the DataFile record(s) will be
            determined automatically.

        :return: A new :class:`DataFile` record.

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
        (123 in this case), he can create a DataFile record as follows:

        mytardis datafile create 123 --storagebox=james-analyzer ~/analysis/dataset1/results.dat

        The file_path argument (set to ~/analysis/dataset1/results.dat)
        specifies the location of 'results.dat' on the analysis server.

        To enable the MyTardis server to access (and verify) the file via
        SSHFS / SFTP, a symbolic link can be created in
        ~james/.mytardisclient/servers/[mytardis_hostname]/, named "dataset1-123" pointing to
        the location of 'results.dat', i.e. ~james/analysis/dataset1/.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        if not dataset_path and os.path.isabs(file_path):
            raise Exception("Either supply dataset_path or supply a relative "
                            "path to the datafile.")
        elif not os.path.exists(file_path):
            raise Exception("Path doesn't exist: %s" % file_path)
        if os.path.isdir(file_path):
            raise Exception("The path should be a single file: %s" % file_path)
        dataset = Dataset.get(dataset_id)
        if dataset_path or os.path.isabs(file_path):
            local_dataset_path = dataset_path
            file_path_without_dataset = os.path.relpath(file_path,
                                                        dataset_path)
            (directory, filename) = os.path.split(file_path_without_dataset)
        else:
            file_path_components = file_path.split(os.sep)
            local_dataset_path = file_path_components.pop(0)
            filename = file_path_components.pop(-1)
            if len(file_path_components) > 0:
                directory = os.path.join(*file_path_components)
            else:
                directory = ""

        uri = os.path.join("%s-%s" % (dataset.description, dataset_id),
                           directory, filename)
        dataset_symlink_path = \
            os.path.join(config.datasets_path,
                         "%s-%s" % (dataset.description, dataset_id))
        if not os.path.exists(dataset_symlink_path):
            print("Creating symlink to: %s in " \
                "~/.config/mytardisclient/servers/%s/ called %s" \
                % (local_dataset_path, config.hostname,
                   "%s-%s" % (dataset.description, dataset_id)))
            os.symlink(os.path.abspath(local_dataset_path),
                       os.path.join(config.datasets_path,
                                    "%s-%s" % (dataset.description,
                                               dataset_id)))
        if DataFile.exists(dataset_id, directory, filename):
            if directory and directory != "":
                _file_path = os.path.join(directory, filename)
            else:
                _file_path = filename
            raise DuplicateKey("A DataFile record already exists for file "
                               "'%s' in dataset ID %s." % (_file_path,
                                                           dataset_id))
        md5sum = md5_sum(file_path)
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
        logger.debug("POST %s %s", url, response.status_code)
        if response.status_code != 201:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        logger.info("Created a DataFile record for %s", file_path)
        if return_new_datafile:
            datafile_id = response.headers['location'].split("/")[-2]
            new_datafile = DataFile.get(datafile_id)
            return new_datafile

    @staticmethod
    def download(datafile_id):
        """
        Download datafile with id datafile_id

        :param datafile_id: The ID of a datafile to download.
        """
        url = "%s/api/v1/dataset_file/%s/download/" \
            % (config.url, datafile_id)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.get(url=url, headers=headers, stream=True)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        try:
            _, params = cgi.parse_header(
                response.headers.get('Content-Disposition', ''))
            filename = params['filename']
        except KeyError:
            print("response.headers: %s" % response.headers)
            raise
        fileobj = open(filename, 'wb')
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fileobj.write(chunk)
        print("Downloaded: %s" % filename)

    @staticmethod
    def upload(dataset_id, storagebox, dataset_path, file_path):
        """
        Upload datafile to dataset with ID dataset_id,
        using HTTP POST.

        :param dataset_id: The ID of the dataset to create the datafile in.
        :param dataset_path:
            Only required if the supplied path to the datafile is absolute
            (not relative).  If a relative path is supplied,
            e.g. 'dataset1/subdir1/datafile1.txt', then the dataset_path
            is assumed to be the first component of the relative path,
            leaving the remaining path components to define the directory
            and filename to record in the DataFile record.
        :param file_path: The local path to the file to be represented in
            the DataFile record.  If dataset_path is not specified,
            file_path must be a relative (not absolute) path, e.g.
            'dataset1/subdir1/datafile1.txt'.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        if not dataset_path and os.path.isabs(file_path):
            raise Exception("Either supply dataset_path or supply a relative "
                            "path to the datafile.")
        elif not os.path.exists(file_path):
            raise Exception("Path doesn't exist: %s" % file_path)
        url = "%s/api/v1/dataset_file/" % config.url
        created_time = datetime.fromtimestamp(
            os.stat(file_path).st_ctime).isoformat()
        if os.path.isabs(file_path):
            file_path_without_dataset = os.path.relpath(file_path,
                                                        dataset_path)
            directory, filename = os.path.split(file_path_without_dataset)
        else:
            file_path_components = file_path.split(os.sep)
            filename = file_path_components.pop(-1)
            if len(file_path_components) > 0:
                _ = file_path_components.pop(0)  # local_dataset_path
            if len(file_path_components) > 0:
                directory = os.path.join(*file_path_components)
            else:
                directory = ""
        if DataFile.exists(dataset_id, directory, filename):
            if directory and directory != "":
                _file_path = os.path.join(directory, filename)
            else:
                _file_path = filename
            raise DuplicateKey("A DataFile record already exists for file "
                               "'%s' in dataset ID %s." % (_file_path,
                                                           dataset_id))
        md5sum = md5_sum(file_path)
        file_data = {"dataset": "/api/v1/dataset/%s/" % dataset_id,
                     "filename": filename,
                     "directory": directory,
                     "md5sum": md5sum,
                     "size": str(os.stat(file_path).st_size),
                     "mimetype": mimetypes.guess_type(file_path)[0],
                     "created_time": created_time}
        if storagebox:
            file_data['replicas'] = [
                {
                    "url": "",
                    "protocol": "file",
                    "location": storagebox
                }
            ]
        file_obj = open(file_path, 'rb')
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.post(url, headers=headers,
                                 data={"json_data": json.dumps(file_data)},
                                 files={'attached_file': file_obj})
        logger.debug("POST %s %s", url, response.status_code)
        file_obj.close()
        if response.status_code != 201:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        if directory:
            print("Uploaded: %s/%s" % (directory, file_path))
        else:
            print("Uploaded: %s" % file_path)

    @staticmethod
    def update(datafile_id, md5sum):
        """
        Update a DataFile record.

        :param datafile_id: The ID of a datafile to be updated.
        :param md5sum: The new MD5 sum value.

        This method is not usable yet, because the MyTardis API doesn't yet
        allow update_detail to be performed on DataFile records.

        For a large file, its upload can commence before the local MD5 sum
        calculation is complete, i.e.  the DataFile record can be initially
        created with a bogus checksum which is later updated using this
        method.
        """
        updated_fields_json = {'md5sum': md5sum}
        url = "%s/api/v1/dataset_file/%s/" % \
            (config.url, datafile_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        logger.debug("PATCH %s %s", url, response.status_code)
        if response.status_code != 202:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        datafile_json = response.json()
        return DataFile(datafile_json)

    @staticmethod
    def verify(datafile_id):
        """
        Ask MyTardis to verify a datafile with id datafile_id

        :param datafile_id: The ID of a datafile to be verified.
        """
        url = "%s/api/v1/dataset_file/%s/verify/" \
            % (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        print("Requested verification of datafile ID %s." % datafile_id)

    @staticmethod
    def exists(dataset_id, directory, filename):
        """
        If MyTardis is running with DEBUG=False, then we won't
        be able detect duplicate key errors easily, we will just
        receive a generic HTTP 500 from the MyTardis API. This
        method checks whether a DataFile record already exists
        for the supplied dataset_id, directory and filename.

        :param dataset_id: The ID of the dataset to check existence in.
        :param directory: The directory within the dataset to check existence in.
        :param filename: The filename to check for existence.

        :return: True if a matching DataFile record already exists.
        """

        url = "%s/api/v1/dataset_file/?format=json" % config.url
        url += "&dataset__id=%s" % dataset_id
        url += "&filename=%s" % urllib2.quote(filename)
        if directory and directory != "":
            url += "&directory=%s" % urllib2.quote(directory)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code < 200 or response.status_code >= 300:
            raise Exception("Failed to check for existing file '%s' "
                            "in dataset ID %s." % (filename, dataset_id))
        return response.json()['meta']['total_count'] > 0


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

        :param datafile_id: The ID of a datafile to list parameter sets for.

        :return: A list of :class:`DatasetParameterSet` records,
            encapsulated in a `ResultSet` object`.
        """
        url = "%s/api/v1/datafileparameterset/?format=json" % config.url
        url += "&datafiles__id=%s" % datafile_id
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("HTTP %s" % response.status_code)
            print("URL: %s" % url)
            message = response.text
            raise Exception(message)
        return ResultSet(DataFileParameterSet, url, response.json())


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

        :param datafile_param_set: The datafile parameter set to
            list parameters for.
        """
        pass
