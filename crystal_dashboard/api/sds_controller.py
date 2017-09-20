# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from swiftclient import client
from horizon.utils.memoized import memoized  # noqa
import requests
import json
import urllib


@memoized
def sds_controller_api(request):
    return request.user.token.id


# # Registry - Global Controllers
def dsl_add_global_controller(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controllers/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def dsl_get_all_global_controllers(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controllers"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_global_controller(request, controller_id, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_global_controller(request, controller_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_global_controller(request, controller_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/global_controller/" + str(controller_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Swift - Sorting Methods
def bw_add_sort_method(request, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/sort_nodes"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def bw_get_all_sort_method(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/sort_nodes"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def bw_update_sort_method(request, name, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/sort_nodes/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def bw_get_sort_method(request, name):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/sort_nodes/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def bw_delete_sort_method(request, name):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/sort_nodes/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Swift - Tenants/ Projects
def is_sds_project(project_name):
    try:
        keystone_admin_url = settings.OPENSTACK_KEYSTONE_URL
        admin_user = settings.IOSTACK_KEYSTONE_ADMIN_USER
        admin_password = settings.IOSTACK_KEYSTONE_ADMIN_PASSWORD
        os_options = {'tenant_name': project_name}
        url, token = client.get_auth(keystone_admin_url, admin_user, admin_password, os_options=os_options, auth_version="2.0")
        head = client.head_account(url, token)
        return 'x-account-meta-storlet-enabled' in head
    except Exception:
        # If the admin user is not assigned to the project (auth exception), then is not a SDS project
        return False


def swift_list_tenants(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/tenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def enable_sds(request, tenant_name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/tenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"tenant_name": tenant_name}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def new_storage_policy(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/spolicies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


# # Swift - Storage Policies
def swift_list_storage_policies(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/storage_policies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# # Swift - Nodes
def swift_get_all_nodes(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_get_node_detail(request, server, node_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes/" + str(server) + "/" + str(node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def swift_update_node(request, server, node_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes/" + str(server) + "/" + str(node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def swift_delete_node(request, server, node_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/swift/nodes/" + str(server) + "/" + str(node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def swift_restart_node(request, node_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + '/swift/nodes/' + str(node_id) + '/restart'

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


# ############################# # Registry DSL API # ##############################
# # Registry DSL - Storage Nodes


def registry_storage_node(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/snode"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def list_storage_nodes(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/snode"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.get(url, headers=headers)
    return r


def remove_storage_nodes(request, storage_node_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/snode/" + str(storage_node_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Policies
def dsl_add_policy(request, policy):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/dynamic_policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, policy, headers=headers)
    return r


# # Registry DSL - Static Policies
def dsl_get_all_static_policies(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/static_policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_static_policy(request, policy_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/static_policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_static_policy(request, policy_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/static_policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_static_policy(request, policy_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/static_policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Dynamic Policies
def list_dynamic_policies(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/dynamic_policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def remove_dynamic_policy(request, policy_id):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/dynamic_policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry - Metric Modules
def mtr_add_metric_module_metadata(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def mtr_get_all_metric_modules(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def mtr_update_metric_module(request, metric_module_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def mtr_get_metric_module(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def mtr_delete_metric_module(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module/" + str(metric_module_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def mtr_download_metric_module_data(request, metric_module_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metric_module/" + str(metric_module_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


# # Registry DSL - Metrics Workload
def dsl_add_workload_metric(request, name, network_location, metric_type):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metrics"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "network_location": str(network_location), "type": str(metric_type)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_workload_metrics(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metrics"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_workload_metric(request, metric_name, network_location=None, metric_type=None):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {}
    if network_location is not None:
        parameters["network_location"] = str(network_location)
    if metric_type is not None:
        parameters["type"] = str(metric_type)

    if len(parameters) == 0:
        raise ValueError

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_metric_metadata(request, metric_name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_workload_metric(request, metric_name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Filters
def dsl_add_filter(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def dsl_get_all_filters(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_filter(request, name, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_filter_metadata(request, name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_filter(request, name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Tenants Groups
def dsl_create_tenants_group(request, name, tenants_list):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # parameters = {"name": str(name), "tenants": str(tenants_list)}
    # r = requests.post(url, json.dumps(parameters), headers=headers)

    r = requests.post(url, json.dumps(tenants_list), headers=headers)
    return r


def dsl_get_all_tenants_groups(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_list_tenants_group(request, group_name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_add_tenant_group_member(request, group_name, tenant_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # TODO
    parameters = {"new": str(tenant_id)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_delete_tenants_group(request, group_name):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def dsl_delete_tenant_group_member(request, group_name, tenant_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/gtenants/" + str(group_name) + "/tenants/" + str(tenant_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Object Types
def dsl_get_all_object_types(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_create_object_type(request, name, extensions):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/object_type"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "types_list": extensions}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_object_type(request, object_type_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_object_type(request, object_type_id, extensions):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(extensions), headers=headers)
    return r


def dsl_delete_object_type(request, object_type_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/controller/object_type/" + str(object_type_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# ############################# # Filters API # ##############################


# Filters - Filters
def fil_create_filter(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_upload_filter_data(request, filter_id, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_download_filter_data(request, filter_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def fil_delete_filter(request, filter_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_filter_metadata(request, filter_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_filters(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_filter_metadata(request, filter_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_deploy_filter(request, filter_id, account_id, parameters):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(parameters), headers=headers)

    return r


def fil_deploy_filter_with_container(request, filter_id, account_id, container_id, parameters):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/" + str(container_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_undeploy_filter(request, filter_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/" + str(account_id) + "/undeploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


# # Filters - Dependencies
def fil_create_dependency(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_upload_dependency_data(request, dependency_id, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependency_id) + "/data"

    headers["X-Auth-Token"] = str(token)
    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_delete_dependency(request, dependecy_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_dependency_metadata(request, dependecy_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_dependencies(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_dependency_metadata(request, dependency_id, version, permissions):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"version": str(version), "permissions": str(permissions)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_deploy_dependency(request, dependency_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/deploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_undeploy_dependency(request, dependency_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/undeploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_dependencies(request, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/dependencies/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# SLOs


def fil_add_slo(request, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_get_all_slos(request):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/slos"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_slo(request, dsl_filter, slo_name, target, data):
    token = sds_controller_api(request)

    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/filters/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_get_slo(request, dsl_filter, slo_name, target):
    token = sds_controller_api(request)

    headers = {}

    # url = settings.IOSTACK_CONTROLLER_URL + "/bw/sla/" + str(sla_id)
    url = settings.IOSTACK_CONTROLLER_URL + "/filters/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_delete_slo(request, dsl_filter, slo_name, target):
    token = sds_controller_api(request)

    headers = {}

    # url = settings.IOSTACK_CONTROLLER_URL + "/bw/sla/" + str(sla_id)
    url = settings.IOSTACK_CONTROLLER_URL + "/filters/slo/" + str(dsl_filter) + "/" + str(slo_name) + "/" + urllib.quote(target)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# ############################## Analytics jobs API ###############################


def anj_submit_job(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def anj_list_job_history(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def anj_clear_job_history(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/jobs"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def anj_list_analyzers(request):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def anj_add_analyzer(request, data, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/data"

    headers["X-Auth-Token"] = str(token)
    # Content-Type header will be set to multipart by django because a file is uploaded

    files = {'file': (in_memory_file.name, in_memory_file.read())}
    data_to_send = {'metadata': json.dumps(data)}

    r = requests.post(url, data_to_send, files=files, headers=headers)
    return r


def anj_download_analyzer(request, analyzer_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/" + str(analyzer_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    r = requests.get(url, headers=headers)
    return r


def anj_delete_analyzer(request, analyzer_id):
    token = sds_controller_api(request)
    headers = {}

    url = settings.IOSTACK_CONTROLLER_URL + "/analytics/analyzers/" + str(analyzer_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r
