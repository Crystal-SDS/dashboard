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
# Policies
#
def dsl_get_all_static_policies(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_static_policy(request, policy_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_static_policy(request, policy_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_static_policy(request, policy_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


#
# Dynamic Policies
#
def dsl_add_policy(request, policy):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, policy, headers=headers)
    return r


def list_dynamic_policies(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def remove_dynamic_policy(request, policy_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


#
# Object Types
#
def dsl_get_all_object_types(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_create_object_type(request, name, extensions):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "types_list": extensions}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_object_type(request, object_type_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_object_type(request, object_type_id, extensions):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(extensions), headers=headers)
    return r


def dsl_delete_object_type(request, object_type_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r
