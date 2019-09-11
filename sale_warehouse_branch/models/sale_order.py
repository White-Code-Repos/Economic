# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError


class SaleOrder(models.Model):
	_inherit = "sale.order"
	
	@api.model
	def _default_warehouse_id(self):
		user = self.env.user
		warehouse_ids = self.env['stock.warehouse'].search([('id', '=', user.warehouses_ids.ids)], limit=1)
		return warehouse_ids

	cur_user = fields.Many2one('res.users','Cur User', default=lambda self: self.env.user.id)
	
	@api.onchange('warehouse_id','cur_user')	
	@api.multi
	def _get_warehouse_domain(self):
		for rec in self:
			if rec.cur_user:
				# domain = {
				# 'warehouse_id':[('id','in',rec.cur_user.warehouses_ids.ids)]
				# }
				domain = {}
				return {'domain':domain}
	warehouse_id = fields.Many2one(
       	'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain= _get_warehouse_domain,default=_default_warehouse_id)

    