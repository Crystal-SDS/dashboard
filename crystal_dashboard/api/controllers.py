# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from swiftclient import client
import six.moves.urllib.parse as urlparse
from horizon.utils.memoized import memoized  # noqa
from oslo_utils import timeutils
import requests
import json
import urllib


@memoized
def sds_controller_api(request):
    return request.user.token.id




# -----------------------------------------------------------------------------
#
# Global Controllers
#
def dsl_add_global_controller(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controllers/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def dsl_get_all_global_controllers(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controllers"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_global_controller(request, controller_id, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_global_controller(request, controller_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_global_controller(request, controller_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r