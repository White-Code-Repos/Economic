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

class Picking(models.Model):
	_inherit = "stock.picking"

	backorder_reason_id = fields.Many2one('backorder.reason', string="Reason", readonly="1")
	action = fields.Selection([('backorder', 'Backorder Created'),('nobackorder', "No BackOrder Created")],'Action Done', readonly="1")