from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from crystal_dashboard.api import filters as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class UploadNativeFilter(forms.SelfHandlingForm):
    filter_file = forms.FileField(label=_("File"),
                                  required=True,
                                  allow_empty_file=False)

    dsl_name = forms.CharField(max_length=255,
                               label=_("DSL Name"),
                               widget=forms.TextInput(
                                   attrs={"ng-model": "dsl_name", "not-blank": ""}
                                ))

    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "main", "not-blank": ""}
                           ))

    language = forms.CharField(max_length=255,
                               label=_("Language"),
                               initial='python',
                               widget=forms.HiddenInput(  # hidden
                                            attrs={"ng-model": "language"}))

    dependencies = forms.CharField(max_length=255,
                                   label=_("Dependencies"),
                                   required=False,
                                   help_text=_("A comma separated list of dependencies"),
                                   widget=forms.HiddenInput(
                                       attrs={"ng-model": "dependencies"}
                                   ))

    valid_parameters = forms.CharField(widget=forms.widgets.Textarea(
                              attrs={'rows': 2}),
                              label=_("Valid Parameters"),
                              required=False)

    put = forms.BooleanField(required=False, label="PUT")
    get = forms.BooleanField(required=False, label="GET")
    post = forms.BooleanField(required=False, label="POST")
    head = forms.BooleanField(required=False, label="HEAD")
    delete = forms.BooleanField(required=False, label="DELETE")

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[
            ('False', _('False')),
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    valid_parameters = forms.CharField(widget=forms.widgets.Textarea(
                              attrs={'rows': 2}),
                              label=_("Valid Parameters"),
                              required=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadNativeFilter, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        filter_file = data['filter_file']
        del data['filter_file']

        data['filter_type'] = 'native'

        try:
            response = api.create_filter(request, data)
            filter_id = data['dsl_name']

            if 200 <= response.status_code < 300:
                response = api.upload_filter_data(request, filter_id, filter_file)

                if 200 <= response.status_code < 300:
                    messages.success(request, _('Native filter successfully created.'))
                    return data
                else:
                    exception_txt = response.text
                    # Error uploading --> delete filter
                    api.delete_filter(request, filter_id)
                    raise sdsexception.SdsException(exception_txt)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UploadStorletFilter(forms.SelfHandlingForm):
    filter_file = forms.FileField(label=_("File"),
                                  required=True,
                                  allow_empty_file=False)

    dsl_name = forms.CharField(max_length=255,
                               label=_("DSL Name"),
                               widget=forms.TextInput(
                                   attrs={"ng-model": "dsl_name", "not-blank": ""}
                                ))

    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "main", "not-blank": ""}
                           ))

    interface_version = forms.CharField(max_length=10,
                                        label=_("Interface Version"),
                                        initial='1.0',
                                        required=True,
                                        help_text=_("Interface Version"),
                                        widget=forms.TextInput(
                                            attrs={"ng-model": "interface_version"}
                                        ))

    dependencies = forms.CharField(max_length=255,
                                   label=_("Dependencies"),
                                   required=False,
                                   help_text=_("A comma separated list of dependencies"),
                                   widget=forms.HiddenInput(
                                       attrs={"ng-model": "dependencies"}
                                   ))

    language = forms.ChoiceField(label=_('Language'),
                                 choices=[('java', _('Java')), ('python', _('Python'))],
                                 widget=forms.Select(attrs={
                                     'class': 'switchable',
                                     'data-slug': 'source'}))

    put = forms.BooleanField(required=False, label="PUT")
    get = forms.BooleanField(required=False, label="GET")

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[
            ('False', _('False')),
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    valid_parameters = forms.CharField(widget=forms.widgets.Textarea(
                          attrs={'rows': 2}),
                          label=_("Valid Parameters"),
                          required=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadStorletFilter, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        filter_file = data['filter_file']
        del data['filter_file']

        data['filter_type'] = 'storlet'

        try:
            filter_id = data['dsl_name']
            response = api.create_filter(request, data)

            if 200 <= response.status_code < 300:
                response = api.upload_filter_data(request, filter_id, filter_file)

                if 200 <= response.status_code < 300:
                    messages.success(request, _('Storlet filter successfully created.'))
                    return data
                else:
                    exception_txt = response.text
                    # Error uploading --> delete filter
                    api.delete_filter(request, filter_id)
                    raise sdsexception.SdsException(exception_txt)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateNativeFilter(forms.SelfHandlingForm):
    filter_file = forms.FileField(label=_("File"),
                                  required=False,
                                  allow_empty_file=False)

    dsl_name = forms.CharField(max_length=255,
                               label=_("DSL Name"))

    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."))

    language = forms.CharField(max_length=255,
                               label=_("Language"),
                               initial='python',
                               widget=forms.HiddenInput(  # hidden
                                            attrs={"ng-model": "language"}))

    put = forms.BooleanField(required=False, label="PUT")
    get = forms.BooleanField(required=False, label="GET")
    post = forms.BooleanField(required=False, label="POST")
    head = forms.BooleanField(required=False, label="HEAD")
    delete = forms.BooleanField(required=False, label="DELETE")

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[
            ('False', _('False')),
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    valid_parameters = forms.CharField(widget=forms.widgets.Textarea(
                          attrs={'rows': 2}),
                          label=_("Valid Parameters"),
                          required=False)

    failure_url = 'horizon:crystal:filters:index'

    def handle(self, request, data):

        filter_file = data['filter_file']
        del data['filter_file']

        try:
            filter_id = self.initial['dsl_name']

            response = api.update_filter_metadata(request, filter_id, data)
            if 200 <= response.status_code < 300:
                if filter_file is not None:
                    response = api.upload_filter_data(request, filter_id, filter_file)
                    if response.status_code > 300:  # error
                        raise sdsexception.SdsException(response.text)
                messages.success(request, _('Filter successfully updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)

        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to update filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateStorletFilter(forms.SelfHandlingForm):
    filter_file = forms.FileField(label=_("File"),
                                  required=False,
                                  allow_empty_file=False)

    dsl_name = forms.CharField(max_length=255,
                               label=_("DSL Name"))

    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."))

    interface_version = forms.CharField(max_length=10,
                                        label=_("Interface Version"),
                                        required=True,
                                        help_text=_("Interface Version"))

    dependencies = forms.CharField(max_length=255,
                                   label=_("Dependencies"),
                                   required=False,
                                   help_text=_("A comma separated list of dependencies"),
                                   widget=forms.HiddenInput(
                                       attrs={"ng-model": "dependencies"}
                                   ))

    language = forms.ChoiceField(label=_('Language'),
                                 choices=[('java', _('Java')), ('python', _('Python'))],
                                 widget=forms.Select(attrs={
                                     'class': 'switchable',
                                     'data-slug': 'source'}))

    put = forms.BooleanField(required=False, label="PUT")
    get = forms.BooleanField(required=False, label="GET")

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    reverse = forms.ChoiceField(
        label=_('Reverse'),
        choices=[
            ('False', _('False')),
            ('proxy', _('Proxy Node')),
            ('object', _('Storage Node'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    valid_parameters = forms.CharField(widget=forms.widgets.Textarea(
                          attrs={'rows': 2}),
                          label=_("Valid Parameters"),
                          required=False)

    failure_url = 'horizon:crystal:filters:index'

    def handle(self, request, data):

        filter_file = data['filter_file']
        del data['filter_file']

        try:
            filter_id = self.initial['dsl_name']

            response = api.update_filter_metadata(request, filter_id, data)
            if 200 <= response.status_code < 300:
                if filter_file is not None:
                    response = api.upload_filter_data(request, filter_id, filter_file)
                    if response.status_code > 300:  # error
                        raise sdsexception.SdsException(response.text)
                messages.success(request, _('Filter successfully updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to update filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
