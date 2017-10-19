import json

from django.utils.translation import ugettext_lazy as _
from swiftclient import ClientException

from horizon import exceptions
from openstack_dashboard.api import keystone
from openstack_dashboard.api import swift
from crystal_dashboard.api import filters as api_filters
from crystal_dashboard.api import projects as api_projects
from crystal_dashboard.api import swift as api_swift
from crystal_dashboard.api import policies as api_policies
from crystal_dashboard.api import metrics as api_metrics


# List Options
# ============
class ListOptions(object):
    @staticmethod
    def by_id():
        """
        Gets the attribute identifier

        :return: attribute identifier
        """
        return 'id'

    @staticmethod
    def by_name():
        """
        Gets the attribute identifier

        :return: attribute identifier
        """
        return 'name'


# Filter Type
# ===========
def get_filter_type_choices():
    """
    Get a tuple of filter types

    :return: tuple with filter types
    """
    return ('', 'Select one'), ('Filter Types', [('storlet', 'Storlet'), ('native', 'Native')])


# Filter
# ======
def get_filter_list_choices(request):
    """
    Get a tuple of filters

    :param request: the request which the dashboard is using
    :return: tuple with filters
    """
    return ('', 'Select one'), ('Filters', get_filter_list(request))


def get_filter_list(request):
    """
    Get a list of filters

    :param request: the request which the dashboard is using
    :return: list with filters
    """

    try:
        response = api_filters.list_filters(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get filters.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    filters_list = []
    filters = json.loads(response_text)

    # Iterate filters
    for filter_ in filters:
        print filter_
        filters_list.append((filter_['id'], filter_['filter_name']))
    return filters_list


# DSL Filter
# ==========
def get_dsl_filter_list_choices(request):
    """
    Get a tuple of dsl filters

    :param request: the request which the dashboard is using
    :return: tuple with dsl filters
    """
    return ('', 'Select one'), ('DSL Filters', get_dsl_filter_list(request))


def get_dsl_filter_list(request):
    """
    Get a list of dsl filters

    :param request: the request which the dashboard is using
    :return: list with dsl filters
    """
    try:
        response = api_filters.list_filters(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get dsl filters.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    dsl_filters_list = []
    dsl_filters = json.loads(response_text)
    # Iterate dsl filters
    for dsl_filter in dsl_filters:
        dsl_filters_list.append((dsl_filter['dsl_name'], dsl_filter['dsl_name']))
    return dsl_filters_list


# Object Type
# ===========
def get_object_type_choices(request):
    """
    Get a tuple of object type choices

    :param request: the request which the dashboard is using
    :return: tuple with object types
    """
    object_type_list = get_object_type_list(request)
    return (('', 'None'), ('Object Types', object_type_list)) if len(object_type_list) > 0 else (('', 'None'),)


def get_object_type_list(request):
    """
    Get a list of object types

    :param request: the request which the dashboard is using
    :return: list with object types
    """
    try:
        response = api_policies.dsl_get_all_object_types(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get object types.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    object_types_list = []
    object_types = json.loads(response_text)
    # Iterate object types
    for object_type in object_types:
        object_types_list.append((object_type['name'], object_type['name']))
    return object_types_list


# Project
# =======
def get_project_list_choices(request):
    """
    Get a tuple of project choices

    :param request: the request which the dashboard is using
    :return: tuple with project choices
    """
    return ('Projects', get_project_list_crystal_enabled(request))


def get_project_list_crystal_enabled(request):
    """
    Get a list of projects

    :param request: the request which the dashboard is using
    :return: list with projects
    """
    try:
        # admin = True (all projects), admin = False (user projects)
        response_text = keystone.tenant_list(request, admin=True)
        enabled_crystal_projects = json.loads(api_projects.list_projects_crystal_enabled(request).text)
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    projects_list = []
    projects = response_text[0]
    # Iterate projects
    for project in projects:
        if project.id in enabled_crystal_projects:
            projects_list.append((project.id, project.name))
    return projects_list


def get_project_list(request):
    """
    Get a list of projects

    :param request: the request which the dashboard is using
    :return: list with projects
    """
    try:
        # admin = True (all projects), admin = False (user projects)
        response_text = keystone.tenant_list(request, admin=True)
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    projects_list = []
    projects = response_text[0]
    # Iterate projects
    for project in projects:
        projects_list.append((project.id, project.name))
    return projects_list


# Container
# =========
def get_container_list_choices(request):
    """
    Get a tuple of container choices

    :param request: the request which the dashboard is using
    :return: tuple with container choices
    """
    return ('', 'Select one'), ('Containers', get_container_list(request))


def get_container_list(request):
    """
    Get a list of containers

    :param request: the request which the dashboard is using
    :return: list with containers
    """
    try:
        swift_headers, swift_containers = swift.swift_api(request).get_account(full_listing=True)
    except ClientException:
        swift_containers = []

    containers_list = []
    # Iterate containers
    for container in swift_containers:
        containers_list.append((container['name'], container['name']))
    return containers_list


# Storage Policy
# ==============
def get_storage_policy_list_choices(request, by_attribute):
    """
    Get a tuple of storage policy choices

    :param request: the request which the dashboard is using
    :param by_attribute: filter by attribute
    :return: tuple with storage policy choices
    """
    return ('', 'Select one'), ('Storage Policies', get_storage_policy_list(request, by_attribute))


def get_storage_policy_list(request, by_attribute):
    """
    Get a list of storage policies

    :param request: the request which the dashboard is using
    :param by_attribute: filter by attribute
    :return: list with storage policies
    """
    try:
        response = api_swift.swift_list_storage_policies(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get storage policies.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    storage_policies_list = []
    storage_policies = json.loads(response_text)
    # Iterate storage policies
    for storage_policy in storage_policies:
        storage_policies_list.append((storage_policy[str(by_attribute)], storage_policy['name']))
    return storage_policies_list


# Workload Metrics
# ==============
def get_activated_workload_metrics_list_choices(request):
    """
    Get a tuple of activaded workload metric choices

    :param request: the request which the dashboard is using
    :return: tuple with activaded workload metric choices
    """
    
    workload_metrics_choices = [(obj['name'], obj['name']) for obj in json.loads(api_metrics.get_activated_workload_metrics(request).text)]
    return ('', 'Select one'), ('Workload Metrics', workload_metrics_choices)