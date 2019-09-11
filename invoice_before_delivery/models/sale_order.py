# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1
#
##############################################################################


from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError


class SaleOrder(models.Model):
	_inherit = "sale.order"

	is_validated = fields.Boolean(string="Validation OK", default=False)


	@api.multi
	def _action_confirm_wo_delivery(self):
		""" Implementation of additionnal mecanism of Sales Order confirmation.
			This method should be extended when the confirmation should generated
			other documents. In this method, the SO are in 'sale' state (not yet 'done').
		"""
		if self.env.context.get('send_email'):
			self.force_quotation_send()

        # create an analytic account if at least an expense product
		if any([expense_policy != 'no' for expense_policy in self.order_line.mapped('product_id.expense_policy')]):
			if not self.analytic_account_id:
				self._create_analytic_account()

		return True

	@api.multi
	def action_confirm_wo_delivery(self):
		if self._get_forbidden_state_confirm() & set(self.mapped('state')):
			raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

		for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
			order.message_subscribe([order.partner_id.id])
		self.write({
			'state': 'sale',
			'confirmation_date': fields.Datetime.now()
		})
		self._action_confirm_wo_delivery()
		if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
			self.action_done()
		return True


	@api.multi
	def action_delivery_create(self):
		for order in self:
			order.write({'is_validated' : False})
			order.order_line._action_launch_stock_rule()
		super(SaleOrder, self)._action_confirm()