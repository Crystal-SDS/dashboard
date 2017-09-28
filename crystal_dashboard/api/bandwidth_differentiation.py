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

#
# Bandwidth SLOs
#
def fil_add_slo(request, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_get_all_slos(request):
    token = sds_controller_api(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_slo(request, dsl_filter, slo_name, target, data):
    token = sds_controller_api(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_get_slo(request, dsl_filter, slo_name, target):
    token = sds_controller_api(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_delete_slo(request, dsl_filter, slo_name, target):
    token = sds_controller_api(request)

    headers = {}
    url = settings.IOSTACK_CONTROLLER_URL + "/policies/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r