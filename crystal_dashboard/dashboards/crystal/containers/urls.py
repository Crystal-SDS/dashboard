# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.conf.urls import url

from crystal_dashboard.dashboards.crystal.containers import views

urlpatterns = [
    url(r'^((?P<container_name>.+?)/)?(?P<subfolder_path>(.+/)+)?$',
        views.ContainerView.as_view(), name='index'),

    url(r'^(?P<container_name>(.+/)+)?create$',
        views.CreateView.as_view(),
        name='create'),
               
    url(r'^(?P<container_name>[^/]+)/update$', views.UpdateContainerView.as_view(),
        name='update'),
    
    url(r'^(?P<container_name>[^/]+)/update_policy$', views.UpdateContainerPolicy.as_view(),
        name='update_policy'),
               
    url(r'^(?P<container_name>[^/]+)/add_metadata$',
        views.AddMetadataView.as_view(),
        name='add_metadata'),

    url(r'^(?P<container_name>.+?)/(?P<subfolder_path>(.+/)+)'
        '?container_detail$',
        views.ContainerDetailView.as_view(),
        name='container_detail'),

    url(r'^(?P<container_name>[^/]+)/(?P<object_path>.+)/object_detail$',
        views.ObjectDetailView.as_view(),
        name='object_detail'),

    url(r'^(?P<container_name>[^/]+)/(?P<subfolder_path>(.+/)+)?'
        '(?P<object_name>.+)/update$',
        views.UpdateObjectView.as_view(),
        name='object_update'),

    url(r'^(?P<container_name>.+?)/(?P<subfolder_path>(.+/)+)?upload$',
        views.UploadView.as_view(),
        name='object_upload'),

    url(r'^(?P<container_name>.+?)/(?P<subfolder_path>(.+/)+)'
        '?create_pseudo_folder',
        views.CreatePseudoFolderView.as_view(),
        name='create_pseudo_folder'),

    url(r'^(?P<container_name>[^/]+)/'
        r'(?P<subfolder_path>(.+/)+)?'
        r'(?P<object_name>.+)/copy$',
        views.CopyView.as_view(),
        name='object_copy'),

    url(r'^(?P<container_name>[^/]+)/(?P<object_path>.+)/download$',
        views.object_download,
        name='object_download'),
]
