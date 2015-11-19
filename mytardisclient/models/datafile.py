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

from .replica import Replica
from .resultset import ResultSet
# from mytardisclient.logs import logger


class DataFile(object):
    """
    Model class for MyTardis API v1's DataFileResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, datafile_json):
        self.config = config
        self.json = datafile_json
        self.id = datafile_json['id']  # pylint: disable=invalid-name
        self.dataset = datafile_json['dataset']
        self.directory = datafile_json['directory']
        self.filename = datafile_json['filename']
        self.size = datafile_json['size']
        self.md5sum = datafile_json['md5sum']
        self.replicas = []
        for replica_json in datafile_json['replicas']:
            self.replicas.append(Replica(config, replica_json))

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
    def list(config, dataset_id=None, limit=None):
        """
        Get datafiles I have access to
        """
        url = "%s/api/v1/dataset_file/?format=json" % config.mytardis_url
        if dataset_id:
            url += "&dataset__id=%s" % dataset_id
        if limit:
            url += "&limit=%s" % limit
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "url: %s" % url
            message = response.text
            response.close()
            raise Exception(message)

        if dataset_id or limit:
            filters = dict(dataset_id=dataset_id, limit=limit)
            return ResultSet(DataFile, config, url, response.json(),
                             **filters)
        else:
            return ResultSet(DataFile, config, url, response.json())

    @staticmethod
    def get(config, datafile_id):
        """
        Get datafile record with id datafile_id

        Not yet possible as the MyTardis API doesn't
        allow filtering on the id field.
        """
        url = "%s/api/v1/dataset_file/?format=json&id=%s" \
            % (config.mytardis_url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            response.close()
            raise Exception(message)

        datafiles_json = response.json()
        return DataFile(config=config, datafile_json=datafiles_json['objects'][0])

    @staticmethod
    def download(config, datafile_id):
        """
        Download datafile with id datafile_id
        """
        url = "%s/api/v1/dataset_file/%s/download/" \
            % (config.mytardis_url, datafile_id)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key)}
        response = requests.get(url=url, headers=headers, stream=True)
        if response.status_code != 200:
            print "url: %s" % url
            message = response.text
            response.close()
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
            if chunk: # filter out keep-alive new chunks
                fileobj.write(chunk)
        print "Downloaded: %s" % filename

    @staticmethod
    def upload(config, dataset_id, file_path):
        """
        Upload datafile to dataset with ID dataset_id.
        """
        url = "%s/api/v1/dataset_file/" % config.mytardis_url
        created_time = datetime.fromtimestamp(
            os.stat(file_path).st_ctime).isoformat()
        md5sum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        file_data = {"dataset": "/api/v1/dataset/%s/" % dataset_id,
                     "filename": os.path.basename(file_path),
                     "directory": "",
                     "md5sum": md5sum,
                     "size": str(os.stat(file_path).st_size),
                     "mimetype": mimetypes.guess_type(file_path)[0],
                     "created_time": created_time}
        file_obj = open(file_path, 'rb')
        response = requests.post(url, headers=config.default_headers,
                                 data={"json_data": json.dumps(file_data)},
                                 files={'attached_file': file_obj})
        file_obj.close()
        if response.status_code != 201:
            print "url: %s" % url
            print "HTTP %s" % response.status_code
            message = response.text
            response.close()
            raise Exception(message)
        print "Uploaded: %s" % file_path

    @staticmethod
    def update(config, datafile_id, md5sum):
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
            (config.mytardis_url, datafile_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        datafile_json = response.json()
        return DataFile(config, datafile_json)
