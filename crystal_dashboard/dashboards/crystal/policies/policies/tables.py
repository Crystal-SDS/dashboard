import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import tables
from models import StaticPolicy
from crystal_dashboard.api import policies as api
from crystal_dashboard.dashboards.crystal import common


class MyStaticPolicyFilterAction(tables.FilterAction):
    name = "my_static_policy_filter"


class CreateStaticPolicy(tables.LinkAction):
    name = "create_static_policy"
    verbose_name = _("Create Policy")
    url = "horizon:crystal:policies:policies:create_static_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class CreatePolicyDSL(tables.LinkAction):
    name = "create_dsl"
    verbose_name = _("Create Policy (DSL)")
    url = "horizon:crystal:policies:policies:create_dsl_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateStaticPolicy(tables.LinkAction):
    name = "update_static_policy"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:crystal:policies:policies:update_static_policy", kwargs={'policy_id': datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, datum, cell):
        return ((cell.column.name == 'object_type') or
                (cell.column.name == 'object_size') or
                (cell.column.name == 'execution_server') or
                (cell.column.name == 'execution_server_reverse') or
                (cell.column.name == 'execution_order') or
                (cell.column.name == 'params'))

    def update_cell(self, request, datum, policy_id, cell_name, new_cell_value):
        try:
            # Updating changed value by new value
            # response = api.dsl_get_static_policy(request, policy_id)
            # data = json.loads(response.text)
            # data[cell_name] = new_cell_value

            api.dsl_update_static_policy(request, policy_id, {cell_name: new_cell_value})
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Can't change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, policy_id):
        response = api.dsl_get_static_policy(request, policy_id)
        data = json.loads(response.text)
        policy = StaticPolicy(data['id'], data['target_id'], data['target_name'], data['filter_name'],
                              data['object_type'], data['object_size'], data['execution_server'],
                              data['execution_server_reverse'], data['execution_order'], data['params'])

        # Overwrite choices for object_type
        choices = common.get_object_type_choices(request)
        self.table.columns['object_type'].form_field.choices = choices

        return policy


class DeleteStaticPolicy(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Policy",
            u"Delete Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Policy",
            u"Deleted Policies",
            count
        )

    name = "delete_static_policy"
    success_url = "horizon:crystal:policies:index"

    def delete(self, request, obj_id):
        try:
            response = api.dsl_delete_static_policy(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted policy/rule: %s') % obj_id)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to remove policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleStaticPolicies(DeleteStaticPolicy):
    name = "delete_multiple_static_policies"


class DeleteDynamicPolicy(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Policy",
            u"Delete Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Policy",
            u"Deleted Policies",
            count
        )

    name = "delete_dynamic_policy"
    success_url = "horizon:crystal:policies:index"

    def delete(self, request, obj_id):
        try:
            response = api.remove_dynamic_policy(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted policy/rule: %s') % obj_id)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:crystal:policies:index")
            error_message = "Unable to remove policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleDynamicPolicies(DeleteDynamicPolicy):
    name = "delete_multiple_dynamic_policies"


class StaticPoliciesTable(tables.DataTable):
    # target_name = tables.Column('target_name', verbose_name=_("Target"))
    target_name = tables.Column(lambda x: str(str(x.target_name) + str(x.target_id).replace(str(x.target_id).split(':')[0], '')).replace(':', '/'), verbose_name=_("Target"))
    filter_name = tables.Column('filter_name', verbose_name=_("Filter"))
    object_type = tables.Column('object_type', verbose_name="Object Type", form_field=forms.ChoiceField(required=False, choices=[]), update_action=UpdateCell)
    object_size = tables.Column('object_size', verbose_name=_("Object Size"), form_field=forms.CharField(max_length=255, required=False), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name="Execution Server", form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_server_reverse = tables.Column('execution_server_reverse', verbose_name="Execution Server Reverse", form_field=forms.ChoiceField(choices=[('none', _('None')), ('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_order = tables.Column('execution_order', verbose_name="Execution Order", form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    params = tables.Column('params', verbose_name="Parameters", form_field=forms.CharField(max_length=300, required=False), update_action=UpdateCell)

    class Meta:
        name = "static_policies"
        verbose_name = _("Static Policies")
        table_actions = (MyStaticPolicyFilterAction, CreateStaticPolicy, CreatePolicyDSL, DeleteMultipleStaticPolicies,)
        row_actions = (UpdateStaticPolicy, DeleteStaticPolicy,)
        row_class = UpdateRow
        hidden_title = False


class MyDynamicPolicyFilterAction(tables.FilterAction):
    name = "my_dynamic_policy_filter"


class DynamicPoliciesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    target = tables.Column('target', verbose_name=_("Target"))
    condition = tables.Column('condition', verbose_name=_("Condition"))
    filter = tables.Column('filter', verbose_name=_("Filter"))
    object_type = tables.Column('object_type', verbose_name=_("Object Type"))
    object_size = tables.Column('object_size', verbose_name=_("Object Size"))
    transient = tables.Column('transient', verbose_name=_("Transient"))
    policy_location = tables.Column('policy', verbose_name=_("DSL Policy"))
    alive = tables.Column('alive', verbose_name="Alive")

    class Meta:
        name = "dynamic_policies"
        verbose_name = _("Dynamic Policies")
        table_actions = (CreatePolicyDSL, MyDynamicPolicyFilterAction, DeleteMultipleDynamicPolicies,)
        row_actions = (DeleteDynamicPolicy,)
        hidden_title = False
