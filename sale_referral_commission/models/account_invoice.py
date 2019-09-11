# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from docutils.nodes import field
import datetime


class AccountInvoice(models.Model):
	_inherit = 'account.invoice'
	
	ref_commission_ids = fields.One2many('referral.commission','invoice_id', string='Referral Commissions',help="Referral Commission related to this order")
