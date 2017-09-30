from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from models import Filter
import json

from crystal_dashboard.api import filters as api
from crystal_dashboard.dashboards.crystal import exceptions as sdsexception


class MyStorletFilterAction(tables.FilterAction):
    name = "my_storlet_filter"


class MyNativeFilterAction(tables.FilterAction):
    name = "my_native_filter"


class UploadFilter(tables.LinkAction):
    name = "upload"
    classes = ("ajax-modal",)
    icon = "upload"


class UploadStorletFilter(UploadFilter):
    verbose_name = _("Upload Storlet Filter")
    url = "horizon:crystal:filters:filters:upload_storlet"


class UploadNativeFilter(UploadFilter):
    verbose_name = _("Upload Native Filter")
    url = "horizon:crystal:filters:filters:upload_native"


class DownloadFilter(tables.LinkAction):
    name = "download"
    verbose_name = _("Download")
    icon = "download"

    def get_link_url(self, datum=None):
        base_url = reverse('horizon:crystal:filters:filters:download', kwargs={'filter_id': datum.id})
        return base_url


class DownloadStorletFilter(DownloadFilter):
    pass


class DownloadNativeFilter(DownloadFilter):
    pass


class DeleteFilter(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Filter",
            u"Delete Filters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Filter",
            u"Deleted Filters",
            count
        )

    name = "delete_filter"
    success_url = "horizon:crystal:filters:index"

    def delete(self, request, obj_id):
        try:
            response = api.fil_delete_filter(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted filter: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:filters:index")
            error_message = "Unable to remove filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteStorletFilter(DeleteFilter):
    pass


class DeleteNativeFilter(DeleteFilter):
    pass


class UpdateFilter(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)


class UpdateStorletFilter(UpdateFilter):
    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:filters:filters:update_storlet", kwargs={'filter_id': datum.id})
        return base_url


class UpdateNativeFilter(UpdateFilter):
    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:filters:filters:update_native", kwargs={'filter_id': datum.id})
        return base_url


class DeleteMultipleFilters(DeleteFilter):
    name = "delete_multiple_filters"


class DeleteMultipleStorletFilters(DeleteMultipleFilters):
    pass


class DeleteMultipleNativeFilters(DeleteMultipleFilters):
    pass


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return (cell.column.name in ['interface_version', 'execution_server', 'execution_server_reverse',
                                     'is_pre_put', 'is_post_put', 'is_pre_get', 'is_post_get', 'has_reverse', 'main'])

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            data = {}
            data[cell_name] = new_cell_value
            api.fil_update_filter_metadata(request, id, data)
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Can't change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateStorletRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        response = api.fil_get_filter_metadata(request, id)
        data = json.loads(response.text)
        filter = Filter(data['id'], data['filter_name'], data['language'],
                        data['filter_type'], data['dependencies'],
                        data['interface_version'],
                        data['main'],
                        data['has_reverse'], data['execution_server'],
                        data['execution_server_reverse'],
                        data['is_pre_put'], data['is_post_put'], data['is_pre_get'], data['is_post_get'])
        return filter


class UpdateNativeRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        response = api.fil_get_filter_metadata(request, id)
        data = json.loads(response.text)
        filter = Filter(data['id'], data['filter_name'], data['language'],
                        data['filter_type'], None, None,
                        data['main'],
                        data['has_reverse'], data['execution_server'],
                        data['execution_server_reverse'],
                        data['is_pre_put'], data['is_post_put'], data['is_pre_get'], data['is_post_get'])
        return filter


class StorletFilterTable(tables.DataTable):
    #id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('filter_name', verbose_name=_("Name"))
    # filter_type = tables.Column('filter_type', verbose_name=_("Type"))
    dsl_name = tables.Column('dsl_name', verbose_name=_("DSL Name"))

    interface_version = tables.Column('interface_version', verbose_name=_("Version"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    #dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    language = tables.Column('language', verbose_name=_("Language"))
    main = tables.Column('main', verbose_name=_("Main Class"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    is_pre_put = tables.Column('is_pre_put', verbose_name=_("Put"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    is_post_get = tables.Column('is_post_get', verbose_name=_("Get"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    has_reverse = tables.Column('has_reverse', verbose_name=_("Reverse"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name=_("Exec. Server"), form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_server_reverse = tables.Column('execution_server_reverse', verbose_name=_("Exec. Server - Reverse"), form_field=forms.ChoiceField(choices=[('none', _('None')), ('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)

    class Meta:
        name = "storlet_filters"
        verbose_name = _("Storlet Filters")
        table_actions = (MyStorletFilterAction, UploadStorletFilter, DeleteMultipleStorletFilters,)
        row_actions = (UpdateStorletFilter, DownloadStorletFilter, DeleteStorletFilter,)
        row_class = UpdateStorletRow
        hidden_title = False


class NativeFilterTable(tables.DataTable):
    #id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('filter_name', verbose_name=_("Name"))
    dsl_name = tables.Column('dsl_name', verbose_name=_("DSL Name"))

    # filter_type = tables.Column('filter_type', verbose_name=_("Type"))
    #interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    #dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    main = tables.Column('main', verbose_name=_("Main Class"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    is_pre_put = tables.Column('is_pre_put', verbose_name=_("pre-PUT"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                               update_action=UpdateCell)
    is_post_put = tables.Column('is_post_put', verbose_name=_("post-PUT"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                               update_action=UpdateCell)
    is_pre_get = tables.Column('is_pre_get', verbose_name=_("pre-GET"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                               update_action=UpdateCell)
    is_post_get = tables.Column('is_post_get', verbose_name=_("post-GET"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                                update_action=UpdateCell)
    has_reverse = tables.Column('has_reverse', verbose_name=_("Reverse"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name=_("Exec. Server"), form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_server_reverse = tables.Column('execution_server_reverse', verbose_name=_("Exec. Server - Reverse"), form_field=forms.ChoiceField(choices=[('none', _('None')), ('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)

    class Meta:
        name = "native_filters"
        verbose_name = _("Native Filters")
        table_actions = (MyNativeFilterAction, UploadNativeFilter, DeleteMultipleNativeFilters,)
        row_actions = (UpdateNativeFilter, DownloadNativeFilter, DeleteNativeFilter,)
        row_class = UpdateNativeRow
        hidden_title = False
