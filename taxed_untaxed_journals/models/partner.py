# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################


from ast import literal_eval
from operator import itemgetter
import time

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP

class AccountFiscalPosition(models.Model):

	_inherit = 'account.fiscal.position'

	journal_ids = fields.One2many('account.fiscal.position.journal', 'position_id', string='Journal Mapping', copy=True)

	@api.model
	def map_journal(self, journal):
		for pos in self.journal_ids:
			if pos.journal_src_id == journal:
				return pos.journal_dest_id
		return journal

	@api.model
	def map_journals(self, journals):
		""" Receive a dictionary having journals in values and try to replace those journals accordingly to the fiscal position."""
		ref_dict = {}
		for line in self.journal_ids:
			ref_dict[line.journal_src_id] = line.journal_dest_id
		for key, jor in journals.items():
			if jor in ref_dict:
				journals[key] = ref_dict[jor]
		return journals	


class AccountFiscalPositionJournal(models.Model):
	_name = 'account.fiscal.position.journal'
	_description = 'Journals Mapping of Fiscal Position'
	_rec_name = 'position_id'

	position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position',
        required=True, ondelete='cascade')
	journal_src_id = fields.Many2one('account.journal', string='Journal on Product', required=True)
	journal_dest_id = fields.Many2one('account.journal', string='Journal to Use Instead', required=True)

	_sql_constraints = [
        ('journal_src_dest_uniq',
         'unique (position_id,journal_src_id,journal_dest_id)',
         'Journal fiscal position could be defined only one time on same journals.')
    ]