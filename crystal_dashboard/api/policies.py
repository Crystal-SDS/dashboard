from __future__ import unicode_literals
from django.conf import settings
import six.moves.urllib.parse as urlparse
from horizon.utils.memoized import memoized  # noqa
import requests
import json
import urllib


@memoized
def get_token(request):
    return request.user.token.id


# -----------------------------------------------------------------------------
#
# Policies
#
def dsl_get_all_static_policies(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_static_policy(request, policy_id, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_static_policy(request, policy_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/static/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_static_policy(request, policy_id):
    token = get_token(request)

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
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, policy, headers=headers)
    return r

def create_dynamic_policy(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r

def update_dynamic_policy(request, policy_id, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r

def list_dynamic_policies(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def remove_dynamic_policy(request, policy_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/dynamic/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


#
# Access Control
#
def create_access_control_policy(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/acl"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r

def access_control_policy_list(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/acl"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r

def delete_access_control(request, policy_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/acl/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r

#
# Object Types
#
def dsl_get_all_object_types(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_create_object_type(request, name, extensions):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "types_list": extensions}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_object_type(request, object_type_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_object_type(request, object_type_id, extensions):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(extensions), headers=headers)
    return r


def dsl_delete_object_type(request, object_type_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


#
# Bandwidth SLOs
#
def fil_add_slo(request, data):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_get_all_slos(request):
    token = get_token(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_slo(request, dsl_filter, slo_name, target, data):
    token = get_token(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_get_slo(request, dsl_filter, slo_name, target):
    token = get_token(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_delete_slo(request, dsl_filter, slo_name, target):
    token = get_token(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r
