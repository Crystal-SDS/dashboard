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
# Metrics
#
def add_metric_module_metadata(request, data, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded
    print in_memory_file
    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.put(url, data_to_send, files=files, headers=headers)
    return r


def get_all_metric_modules(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def update_metric_module(request, metric_module_id, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def get_metric_module(request, metric_module_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def delete_metric_module(request, metric_module_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def download_metric_module_data(request, metric_module_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def get_activated_workload_metrics(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/activated"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r
