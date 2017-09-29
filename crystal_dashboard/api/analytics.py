from __future__ import unicode_literals
from django.conf import settings
from horizon.utils.memoized import memoized  # noqa
import requests
import json


@memoized
def get_token(request):
    return request.user.token.id


def anj_submit_job(request, data, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def anj_list_job_history(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def anj_clear_job_history(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def anj_list_analyzers(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def anj_add_analyzer(request, data, in_memory_file):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def anj_download_analyzer(request, analyzer_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/" + str(analyzer_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def anj_delete_analyzer(request, analyzer_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/" + str(analyzer_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r