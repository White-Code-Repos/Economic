# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.addons import decimal_precision as dp
import logging

class AccountInvoice(models.Model):
	_inherit = "account.invoice"
    
	@api.onchange('fiscal_position_id')
	def _onchange_fiscal_position_id(self):
		if self.fiscal_position_id:
			for inv in self:
				for pos in inv.fiscal_position_id:
					if pos.journal_ids.journal_src_id == inv.journal_id:
						inv.journal_id = pos.journal_ids.journal_dest_id

	@api.model
	def create(self, vals):
		res = super(AccountInvoice, self).create(vals)
		if vals.get('fiscal_position_id'):
			pos = self.env['account.fiscal.position'].search([('id', '=', vals.get('fiscal_position_id'))])
			if pos.journal_ids.journal_src_id == res.journal_id:
				res.journal_id = pos.journal_ids.journal_dest_id
		return res

