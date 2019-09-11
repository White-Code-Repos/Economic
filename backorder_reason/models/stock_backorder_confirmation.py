# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare

class StockBackorderConfirmation(models.TransientModel):
	_inherit = 'stock.backorder.confirmation'

	backorder_reason_id = fields.Many2one('backorder.reason', string="Reason", required="1")
	
	def process(self):
		for pick_id in self.pick_ids:
			reason_val = self.backorder_reason_id
			# backorder_pick = self.env['stock.picking'].search([('backorder_id', '=', pick_id.id)])
			pick_id.write({'backorder_reason_id':reason_val.id,
								  'action': 'backorder'})
		self._process()
	def process_cancel_backorder(self):
		reason_val = self.backorder_reason_id
		for pick_id in self.pick_ids:
			pick_id.write({'backorder_reason_id':reason_val.id,
							'action': 'nobackorder'})
		self._process(cancel_backorder=True)
