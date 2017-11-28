from __future__ import unicode_literals
from django.conf import settings
import six.moves.urllib.parse as urlparse
from horizon.utils.memoized import memoized  # noqa
from openstack_dashboard.api.swift import swift_api
from openstack_dashboard.api.swift import Container
from openstack_dashboard.api.swift import GLOBAL_READ_ACL
from openstack_dashboard.api import base
from oslo_utils import timeutils
import requests
import json


@memoized
def get_token(request):
    return request.user.token.id


# -----------------------------------------------------------------------------
#
# Swift - Regions
#
def swift_list_regions(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/regions"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def new_region(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/regions"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)

    return r


def delete_region(request, region_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/regions/" + str(region_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def update_region(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/regions/" + str(data['region_id'])

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def get_region(request, region_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/regions/" + str(region_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


#
# Swift - Zones
#
def swift_list_zones(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/zones"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def new_zone(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/zones"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)

    return r


def delete_zone(request, zone_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/zones/" + str(zone_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def update_zone(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/zones/" + str(data['zone_id'])

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def get_zone(request, zone_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/zones/" + str(zone_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


#
# Swift - Nodes
#
def swift_get_all_nodes(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_get_node_detail(request, server_type, node_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes/" + str(server_type) + "/" + str(node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_update_node(request, server_type, node_id, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes/" + str(server_type) + "/" + str(node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def swift_restart_node(request, server_type, node_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + '/swift/nodes/' + str(server_type) + "/" + str(node_id) + '/restart'

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


#
# Swift - Storage Policies
#
def swift_new_storage_policy(request, data):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def swift_delete_storage_policy(request, storage_policy_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# TODO
def load_swift_policies(request):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policies/load"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps({}), headers=headers)
    return r


def deploy_storage_policy(request, storage_policy_id):
    token = get_token(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id) + "/deploy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps({}), headers=headers)
    return r


def swift_list_storage_policies(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_list_deployed_storage_policies(request):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policies/deployed"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_available_disks_storage_policy(request, storage_policy_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id) + "/disk/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_storage_policy_detail(request, storage_policy_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_edit_storage_policy(request, storage_policy_id, data):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def swift_add_disk_storage_policy(request, storage_policy_id, disk_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id) + "/disk/"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(disk_id), headers=headers)
    return r


def swift_remove_disk_storage_policy(request, storage_policy_id, disk_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policy/" + str(storage_policy_id) + "/disk/" + disk_id

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


#
# Swift - Containers
#
def swift_get_container(request, container_name, with_data=True):
    if with_data:
        headers, data = swift_api(request).get_object(container_name, "")
    else:
        data = None
        headers = swift_api(request).head_container(container_name)
    timestamp = None
    is_public = False
    public_url = None
    try:
        is_public = GLOBAL_READ_ACL in headers.get('x-container-read', '')
        if is_public:
            swift_endpoint = base.url_for(request,
                                          'object-store',
                                          endpoint_type='publicURL')
            parameters = urlparse.quote(container_name.encode('utf8'))
            public_url = swift_endpoint + '/' + parameters
        ts_float = float(headers.get('x-timestamp'))
        timestamp = timeutils.iso8601_from_timestamp(ts_float)

        metadata = ''
        for header in headers:
            if header.startswith('x-container-meta-'):
                key_name = header.replace('x-container-meta-', '').replace('-', ' ').title()
                value = headers[header]
                metadata += key_name + '=' + value + ', '

        metadata = metadata[0:-2]

    except Exception:
        pass
    container_info = {
        'name': container_name,
        'container_object_count': headers.get('x-container-object-count'),
        'container_bytes_used': headers.get('x-container-bytes-used'),
        'timestamp': timestamp,
        'data': data,
        'is_public': is_public,
        'public_url': public_url,
        'storage_policy': headers.get('x-storage-policy'),
        'metadata': metadata,
    }
    return Container(container_info)


def swift_get_project_containers(request, project_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/" + str(project_id) + "/containers"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_create_container(request, project_id, container_name, container_headers):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/" + project_id + "/" + str(container_name) + "/create"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(container_headers), headers=headers)
    return r


def swift_update_container_policy(request, project_id, container_name, storage_policy_id):
    token = get_token(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/" + project_id + "/" + str(container_name) + "/policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(storage_policy_id), headers=headers)
    return r