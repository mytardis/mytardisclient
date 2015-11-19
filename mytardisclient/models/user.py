"""
Model class for MyTardis API v1's UserResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""
import requests
import traceback
import urllib2

from .group import Group
from mytardisclient.utils.exceptions import IncompatibleMyTardisVersion
from mytardisclient.utils.exceptions import DoesNotExist
from mytardisclient.logs import logger


class User(object):
    """
    Model class for MyTardis API v1's UserResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=missing-docstring
    # pylint: disable=too-many-instance-attributes
    def __init__(self, config=None,
                 username=None, name=None,
                 email=None, user_record_json=None):
        # pylint: disable=too-many-arguments
        self.config = config
        self.user_id = None
        self.username = username
        self.name = name
        self.email = email
        self.groups = []
        self.user_record_json = user_record_json

        if user_record_json is not None:
            self.user_id = user_record_json['id']
            if username is None:
                self.username = user_record_json['username']
            if name is None:
                self.name = user_record_json['first_name'] + " " + \
                    user_record_json['last_name']
            if email is None:
                self.email = user_record_json['email']
            try:
                for group in user_record_json['groups']:
                    self.groups.append(Group(config=config,
                                             group_json=group))
            except KeyError:
                # 'groups' should be available in the user record's JSON
                message = "Incompatible MyTardis version" \
                    "\n\n" \
                    "You appear to be connecting to a MyTardis server whose " \
                    "MyTardis version doesn't provide some of the " \
                    "functionality required by MyData." \
                    "\n\n" \
                    "Please check that you are using the correct MyTardis " \
                    "URL and ask your MyTardis administrator to check " \
                    "that an appropriate version of MyTardis is installed."
                logger.error(traceback.format_exc())
                logger.error(message)
                raise IncompatibleMyTardisVersion(message)

    def __str__(self):
        return "User: " + self.username

    @staticmethod
    def get_user_by_username(config, username):
        url = config.mytardis_url + "/api/v1/user/?format=json&username=" + username
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key)}
        try:
            response = requests.get(url=url, headers=headers)
        except:
            raise Exception(traceback.format_exc())
        if response.status_code != 200:
            message = response.text
            raise Exception(message)
        try:
            user_records_json = response.json()
        except:
            logger.error(traceback.format_exc())
            raise
        num_user_records_found = user_records_json['meta']['total_count']

        if num_user_records_found == 0:
            raise DoesNotExist(
                message="User \"%s\" was not found in MyTardis" % username,
                url=url, response=response)
        else:
            logger.debug("Found user record for username '" + username + "'.")
            return User(config=config, username=username,
                        user_record_json=user_records_json['objects'][0])

    @staticmethod
    def get_user_by_email(config, email):
        url = config.mytardis_url + "/api/v1/user/?format=json&email__iexact=" + \
            urllib2.quote(email)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key)}
        try:
            response = requests.get(url=url, headers=headers)
        except:
            raise Exception(traceback.format_exc())
        if response.status_code != 200:
            logger.debug(url)
            message = response.text
            raise Exception(message)
        try:
            user_records_json = response.json()
        except:
            logger.error(traceback.format_exc())
            raise
        num_user_records_found = user_records_json['meta']['total_count']

        if num_user_records_found == 0:
            raise DoesNotExist(
                message="User with email \"%s\" was not found in MyTardis"
                % email,
                url=url, response=response)
        else:
            logger.debug("Found user record for email '" + email + "'.")
            return User(config=config,
                        user_record_json=user_records_json['objects'][0])


# pylint: disable=too-few-public-methods
class UserProfile(object):
    """
    Used with the DoesNotExist exception when a 404 from MyTardis's API
    is assumed to have been caused by a missing user profile record.
    """
    pass
