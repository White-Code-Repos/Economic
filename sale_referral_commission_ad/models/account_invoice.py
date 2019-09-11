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
from docutils.nodes import field
import datetime


class AccountInvoice(models.Model):
	_inherit = 'account.invoice'
	
	ref_commission_ids = fields.One2many('referral.commission','invoice_id', string='Referral Commissions',help="Referral Commission related to this order")