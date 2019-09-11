# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################

# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo import tools
import datetime
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


from odoo.addons import decimal_precision as dp

from werkzeug.urls import url_encode


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ref_commission_ids = fields.One2many('referral.commission','order_id', string='Referral Commissions',
                                     help="Referral Commission related to this order")


    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
    	res = super(SaleOrder, self).action_invoice_create()
    	inv_obj = self.env['account.invoice']
    	if res:
    		curr_inv = inv_obj.search([('id', '=', res[0])])
    		if self.ref_commission_ids:
    			curr_inv.write({'ref_commission_ids' : [(6, 0, self.ref_commission_ids.ids)]})