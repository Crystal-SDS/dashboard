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
# Crystal Projects
#
def list_projects_crystal_enabled(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def is_crystal_project(request, project_id):

    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/" + str(project_id)

    headers["X-Auth-Token"] = str(token)

    r = requests.post(url, headers=headers)
    return r


def enable_crystal(request, project_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/" + str(project_id)

    headers["X-Auth-Token"] = str(token)

    r = requests.put(url, headers=headers)
    return r


def disable_crystal(request, project_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/" + str(project_id)

    headers["X-Auth-Token"] = str(token)

    r = requests.delete(url, headers=headers)
    return r


#
# Project Groups
#
def create_projects_group(request, name, tenants_list):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # parameters = {"name": str(name), "tenants": str(tenants_list)}
    # r = requests.post(url, json.dumps(parameters), headers=headers)

    r = requests.post(url, json.dumps(tenants_list), headers=headers)
    return r


def get_all_project_groups(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def list_projects_group(request, group_name):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def add_project_group_member(request, group_name, tenant_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # TODO
    parameters = {"new": str(tenant_id)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def delete_project_group(request, group_name):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def delete_project_group_member(request, group_name, tenant_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_name) + "/projects/" + str(tenant_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r
