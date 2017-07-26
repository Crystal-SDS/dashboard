# Copyright 2012 Nebula, Inc.
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Policies for managing policies.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.api import sds_controller as api


class CreatePolicy(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255, label=_("Policy/Rule"))

    def handle(self, request, data):
        try:
            response = api.create_policy(request, data["policy"])
            print "CAMAMILLA response", response, response.text
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy/rule: %s') % data['policy'])
                return data
            else:
                # FOR 4f0279da74ef4584a29dc72c835fe2c9 WHEN get_ops_tenant > 4 DO SET pepito WITH param1=2
                print "ERROR: sdscontroller.storagepolicies.policies", response, response.text
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)
