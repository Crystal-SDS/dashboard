from __future__ import unicode_literals
from django.conf import settings
import six.moves.urllib.parse as urlparse
from horizon.utils.memoized import memoized  # noqa
import requests
import json


@memoized
def get_token(request):
    return request.user.token.id


# -----------------------------------------------------------------------------
#
# Global Controllers
#
def add_controller(request, data, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def get_all_controllers(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def update_controller(request, controller_id, data, in_memory_file):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def get_controller(request, controller_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def delete_controller(request, controller_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# -----------------------------------------------------------------------------
#
# Instances
#
def get_all_instances(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/instances/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def get_instance(request, instance_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/instance/" + str(instance_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def add_instance(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/instance/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def delete_instance(request, instance_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/instance/" + str(instance_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def update_instance(request, instance_id, data):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controllers/instance/" + str(instance_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r
