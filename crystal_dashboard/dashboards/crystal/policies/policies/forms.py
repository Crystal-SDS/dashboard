from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import policies as api
from crystal_dashboard.api import filters as filters_api
from crystal_dashboard.api import policies as policies_api
from crystal_dashboard.dashboards.crystal import common
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class CreateDSLPolicy(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255,
                             label=_("Policy/Rule"),
                             widget=forms.Textarea(
                                 attrs={"ng-model": "interface_version", "not-blank": ""}
                             ))

    def __init__(self, request, *args, **kwargs):
        super(CreateDSLPolicy, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            response = api.dsl_add_policy(request, data['policy'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy: %s') % data['policy'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateStaticPolicy(forms.SelfHandlingForm):
    target_choices = []
    target_id = forms.ChoiceField(choices=target_choices,
                                  label=_("Project"),
                                  help_text=_("The project where the rule will be applied."),
                                  required=True)

    container_choices = [('', 'None')]
    container_id = forms.CharField(label=_("Container"),
                                   help_text=_("The container where the rule will be applied."),
                                   required=False,
                                   widget=forms.Select(choices=container_choices))

    filter_dsl_choices = []
    filter_id = forms.ChoiceField(choices=filter_dsl_choices,
                                  label=_("Filter"),
                                  help_text=_("The id of the filter which will be used."),
                                  required=True)

    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  required=False,
                                  help_text=_("The size of object the rule will be applied to."))

    object_tag = forms.CharField(max_length=255,
                                 label=_("Object Tag"),
                                 required=False)

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[('default', _('Default')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[('default', _('Default')),
                 ('False', _('False')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    params = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 4}),
                             label=_("Parameters"),
                             required=False,
                             help_text=_("CSV Parameters list.Ex: param1=value1, param2=value2"))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.target_choices = [('', 'Select one'), ('global', 'Global (All Projects)'), common.get_project_list_choices(request), common.get_group_project_choices(request)]

        # Obtain list of dsl filters
        self.dsl_filter_choices = common.get_dsl_filter_list_choices(request)
        # Obtain list of object types
        self.object_type_choices = common.get_object_type_choices(request)

        # Initialization
        super(CreateStaticPolicy, self).__init__(request, *args, **kwargs)

        # Overwrite target_id input form
        self.fields['target_id'] = forms.ChoiceField(choices=self.target_choices,
                                                     # initial=request.user.project_id,  # Default project is the current one
                                                     label=_("Project"),
                                                     help_text=_("The project where the rule will be apply."),
                                                     required=True)
        # Overwrite filter_id input form
        self.fields['filter_id'] = forms.ChoiceField(choices=self.dsl_filter_choices,
                                                     label=_("Filter"),
                                                     help_text=_("The id of the filter which will be used."),
                                                     required=True)
        # Overwrite object_type input form
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    @staticmethod
    def handle(request, data):
        try:
            if data['container_id'] != '':
                response = filters_api.deploy_filter_with_container(request, data['filter_id'], data['target_id'],
                                                                    data['container_id'], data)
            else:
                response = filters_api.deploy_filter(request, data['filter_id'], data['target_id'], data)
    
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created static policy'))
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateDynamicPolicy(forms.SelfHandlingForm):
    project_choices = []
    project_id = forms.ChoiceField(choices=project_choices,
                                   label=_("Project"),
                                   help_text=_("The project where the rule will be applied."),
                                   required=True)

    container_choices = [('', 'None')]
    container_id = forms.CharField(label=_("Container"),
                                   help_text=_("The container where the rule will be applied."),
                                   required=False,
                                   widget=forms.Select(choices=container_choices))

    action = forms.ChoiceField(
        label=_('Action'),
        choices=[('SET', _('Set')),
                 ('DELETE', _('Delete'))],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'action'
        })
    )

    filter_dsl_choices = []
    filter_id = forms.ChoiceField(choices=filter_dsl_choices,
                                  label=_("Filter"),
                                  help_text=_("The id of the filter which will be used."),
                                  required=True)

    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  required=False,
                                  help_text=_("The size of object the rule will be applied to."))

    object_tag = forms.CharField(max_length=255,
                                 label=_("Object Tag"),
                                 required=False,
                                 help_text=_("The metadata tag of object the rule will be applied to."))

    workload_metrics = []
    workload_metric = forms.ChoiceField(choices=workload_metrics,
                                        label=_("Workload Metrics"),
                                        help_text=_(""),
                                        required=True)

    condition = forms.CharField(max_length=255,
                                label=_("Condition"),
                                required=True)

    transient = forms.BooleanField(required=False, label="Transient")

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[('default', _('Default')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[('default', _('Default')),
                 ('False', _('False')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    params = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 2}),
                             label=_("Parameters"),
                             required=False,
                             help_text=_("CSV Parameters list.Ex: param1=value1, param2=value2"))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.project_choices = [('', 'Select one'), ('global', 'Global (All Projects)'), common.get_project_list_choices(request), common.get_group_project_choices(request)]

        # Obtain list of dsl filters
        self.dsl_filter_choices = common.get_dsl_filter_list_choices(request)
        # Obtain list of object types
        self.object_type_choices = common.get_object_type_choices(request)

        self.workload_metrics = common.get_activated_workload_metrics_list_choices(request)

        # Initialization
        super(CreateDynamicPolicy, self).__init__(request, *args, **kwargs)

        # Overwrite project_id input form
        self.fields['project_id'] = forms.ChoiceField(choices=self.project_choices,
                                                      # initial=request.user.project_id,  # Default project is the current one
                                                      label=_("Project"),
                                                      help_text=_("The project where the rule will be apply."),
                                                      required=True)
        # Overwrite filter_id input form
        self.fields['filter_id'] = forms.ChoiceField(choices=self.dsl_filter_choices,
                                                     label=_("Filter"),
                                                     help_text=_("The id of the filter which will be used."),
                                                     required=True)
        # Overwrite object_type input form
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

        self.fields['workload_metric'] = forms.ChoiceField(choices=self.workload_metrics,
                                                           label=_("Workload Metrics"),
                                                           required=True)

    @staticmethod
    def handle(request, data):
        try:
            response = policies_api.create_dynamic_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created dynamic policy'))
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdatePolicy(forms.SelfHandlingForm):
    
    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  required=False,
                                  help_text=_("The size of object which the rule will be apply."))

    object_tag = forms.CharField(max_length=255,
                                 label=_("Object Tag"),
                                 required=False)

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[('default', _('Default')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[('default', _('Default')),
                 ('False', _('False')),
                 ('proxy', _('Proxy Node')),
                 ('object', _('Storage Node'))],
        initial='default',
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    execution_order = forms.CharField(max_length=255,
                                      label=_("Execution Order"),
                                      help_text=_("The order in which the policy will be executed."))

    params = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 4}),
                             label=_("Parameters"),
                             required=False,
                             help_text=_("Parameters list."))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of object types
        self.object_type_choices = common.get_object_type_choices(request)
        # initialization
        super(UpdatePolicy, self).__init__(request, *args, **kwargs)
        # overwrite object_type input form
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    failure_url = 'horizon:crystal:policies:index'

    def handle(self, request, data):
        try:
            policy_id = self.initial['target_id'] + ':' + self.initial['id']
            response = api.dsl_update_static_policy(request, policy_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Policy successfully updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to update policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
