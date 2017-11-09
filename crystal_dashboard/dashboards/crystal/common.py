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


# Groups
# =========
def get_group_project_choices(request):
    return ('Project Groups', get_group_project_list(request))


def get_group_project_list(request):
    response = api_projects.get_all_project_groups(request).text
    groups = json.loads(response)
    groups_choices = [('group:'+group['id'], group['name']) for group in groups]

    return groups_choices


# =========
# Container
# =========
def get_container_list_choices(request, project_id):
    """
    Get a tuple of container choices

    :param request: the request which the dashboard is using
    :return: tuple with container choices
    """
    return ('', 'Select one'), ('Containers', get_container_list(request, project_id))


def get_container_list(request, project_id):
    """
    Get a list of containers

    :param request: the request which the dashboard is using
    :return: list with containers
    """
    try:
        response = api_swift.swift_get_project_containers(request, project_id)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get containers')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    containers_list = []
    containers = json.loads(response_text)
    # Iterate object types
    for container in containers:
        containers_list.append((container['name'], container['name']))
    return containers_list


# =========
# Users
# =========
def get_user_list_choices(request, project_id):
    """
    Get a tuple of user choices

    :param request: the request which the dashboard is using
    :return: tuple with container choices
    """
    return ('', 'Select one'), ('Users', get_users_list(request, project_id))


def get_users_list(request, project_id):
    """
    Get a list of users

    :param request: the request which the dashboard is using
    :return: list with containers
    """
    try:
        response = api_projects.get_project_users(request, project_id)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get users')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    users_list = []
    users = json.loads(response_text)
    # Iterate object types
    for user in users:
        users_list.append(('user_id:'+user['id'], user['name']))
    return users_list


# =========
# User Groups
# =========
def get_groups_list_choices(request, project_id):
    """
    Get a tuple of groups choices

    :param request: the request which the dashboard is using
    :return: tuple with container choices
    """
    return ('', 'Select one'), ('Groups', get_groups_list(request, project_id))


def get_groups_list(request, project_id):
    """
    Get a list of groups

    :param request: the request which the dashboard is using
    :return: list with containers
    """
    try:
        response = api_projects.get_project_groups(request, project_id)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get groups')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    groups_list = []
    groups = json.loads(response_text)
    # Iterate object types
    for group in groups:
        groups_list.append(('group_id:'+group['id'], group['name']))
    return groups_list


# ==============
# Storage Policies
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


# ==============
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
