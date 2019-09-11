# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
class sale_configuration_settings(models.TransientModel):
    _inherit = "res.config.settings"
    referral_commission_account = fields.Many2one('account.account',domain=[('user_type_id', '=', 'Expenses')],string="Referral Commission Account")


    def get_values(self):
        res = super(sale_configuration_settings, self).get_values()
        referral_commission_account= int(self.env['ir.config_parameter'].sudo().get_param('sale_referral_commission.referral_commission_account'))
        res.update(referral_commission_account = referral_commission_account)
        return res

    def set_values(self):
        super(sale_configuration_settings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale_referral_commission.referral_commission_account', self.referral_commission_account.id)