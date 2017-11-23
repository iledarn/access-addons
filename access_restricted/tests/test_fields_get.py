# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from odoo.addons.base.res.res_users import name_selection_groups


class TestFieldsGet(TransactionCase):
    post_install = True

    def test_base(self):
        demo_user = self.env.ref('base.user_demo')
        group_erp_manager = self.env.ref('base.group_erp_manager')
        group_system = self.env.ref('base.group_system')

        demo_user.write({'groups_id': [(4, group_erp_manager.id)]})
        self.env['res.groups'].sudo(demo_user.id)._update_user_groups_view()
        sel_groups = name_selection_groups([group_erp_manager.id])
        res = demo_user.fields_get()
        self.assertTrue(res.get(sel_groups))

        demo_user.write({'groups_id': [(4, group_system.id)]})
        self.env['res.groups'].sudo(demo_user.id)._update_user_groups_view()
        sel_groups = name_selection_groups([group_erp_manager.id, group_system.id])
        res = demo_user.fields_get()
        self.assertTrue(res.get(sel_groups))
