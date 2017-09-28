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
# Filters
#
def fil_create_filter(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_upload_filter_data(request, filter_id, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_download_filter_data(request, filter_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def fil_delete_filter(request, filter_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_filter_metadata(request, filter_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_filters(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_filter_metadata(request, filter_id, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_deploy_filter(request, filter_id, account_id, parameters):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(parameters), headers=headers)

    return r


def fil_deploy_filter_with_container(request, filter_id, account_id, container_id, parameters):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/" + str(container_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_undeploy_filter(request, filter_id, account_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/undeploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


#
# Filters - Dependencies
#
def fil_create_dependency(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_upload_dependency_data(request, dependency_id, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependency_id) + "/data"

    headers["X-Auth-Token"] = str(token)
    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_delete_dependency(request, dependecy_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_dependency_metadata(request, dependecy_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_dependencies(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_dependency_metadata(request, dependency_id, version, permissions):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"version": str(version), "permissions": str(permissions)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_deploy_dependency(request, dependency_id, account_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/deploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_undeploy_dependency(request, dependency_id, account_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/undeploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_dependencies(request, account_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


#
# DSL Mapping
#
def dsl_add_filter(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dsl"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def dsl_get_all_filters(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dsl"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_filter(request, name, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dsl/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_filter_metadata(request, name):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dsl/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_filter(request, name):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dsl/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r
