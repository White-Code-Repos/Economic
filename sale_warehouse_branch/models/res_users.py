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

from odoo import api, fields, models, tools


class Users(models.Model):
	_inherit = 'res.users'


	branch_id = fields.Many2one('user.branch', string="Branch")
	warehouses_ids = fields.Many2many('stock.warehouse', 'users_warehouse_rel', 'uid', 'wid', string="Allowed Warehouses")
