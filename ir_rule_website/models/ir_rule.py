# -*- coding: utf-8 -*-

from odoo import api, models, tools, fields
from odoo.addons.base.ir.ir_rule import IrRule as IrRuleOriginal


class IrRule(models.Model):
    _inherit = 'ir.rule'

    backend_behaviour = fields.Selection([
        ("true", "Grant access"),
        ("false", "Deny access"),
    ], string='Backend behaviour',
        help="""This is bypass for main rule definition.
        When working from backend there is usually no 'website_id' value in the rule evaluation context
        what leads to SQL syntax error such as 'WHERE website_id IN ()' in rules that using 'website_id'""")

    @api.depends('domain_force')
    def _force_domain(self):
        eval_context = self._eval_context()
        if not eval_context.get('website_id'):
            website_rules = self.filtered(lambda r: r.backend_behaviour)
            for rule in website_rules:
                rule.domain = [(1, '=', 1)] if rule.backend_behaviour == 'true' else [(0, '=', 1)]
            super(IrRule, self - website_rules)._force_domain()
        else:
            super(IrRule, self)._force_domain()

    @api.model
    def _eval_context(self):
        context = super(IrRule, self)._eval_context()
        context['website_id'] = self._context.get('website_id')
        return context

    @api.model
    @tools.ormcache_context('self._uid', 'model_name', 'mode', keys=["website_id"])
    def _compute_domain(self, model_name, mode="read"):
        return IrRuleOriginal._compute_domain.__wrapped__(self, model_name, mode=mode)
