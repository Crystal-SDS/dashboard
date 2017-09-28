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
# Metrics
#
def mtr_add_metric_module_metadata(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.put(url, data_to_send, files=files, headers=headers)
    return r


def mtr_get_all_metric_modules(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def mtr_update_metric_module(request, metric_module_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def mtr_get_metric_module(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def mtr_delete_metric_module(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def mtr_download_metric_module_data(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/" + str(metric_module_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def dsl_add_workload_metric(request, name, network_location, metric_type):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/activated"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "network_location": str(network_location), "type": str(metric_type)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_workload_metrics(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/metrics/activated"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r