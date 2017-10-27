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
def create_projects_group(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    data['attached_projects'] = json.dumps(data['attached_projects'])

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def update_projects_group(request, data, group_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    data['attached_projects'] = json.dumps(data['attached_projects'])

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def get_all_project_groups(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def get_project_group(request, group_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def delete_project_group(request, group_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/projects/groups/" + str(group_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r