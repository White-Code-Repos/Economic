# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from docutils.nodes import field
import datetime

from odoo.addons import decimal_precision as dp
class ReferralCommission(models.Model):
	_name = 'referral.commission'



	@api.multi
	def _get_default_account(self):
		referral_commission_account = self.env['res.config.settings'].search([], limit=1, order="id desc").referral_commission_account
		if referral_commission_account:
			return referral_commission_account

	@api.multi
	def _get_default_inv_ref(self):
		if self.invoice_id:
			if self.invoice_id.type == "out_invoice":
				self.is_invoice = True
			else:
				self.is_invoice = False


	name = fields.Char(string="Description", size=512)
	partner_id = fields.Many2one('res.partner', string='Referral Person',
								help="referral person associated with this type of commission",
								required=True)
	date = fields.Date('Date')
	commission_amount = fields.Float(string="Commission Amount", required=True)
	account_id = fields.Many2one('account.account', string='Account')
	order_id = fields.Many2one('sale.order', string='Order Reference',
								help="Affected Sale Order")
	invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
								help="Affected Sale Order")
	account_id = fields.Many2one('account.account', string='Account', help="Select the account", default=_get_default_account)

	journal_id = fields.Many2one('account.journal', string='Payment Method', help="select the payment method for refferal")

	is_validated = fields.Boolean('Is Validated', default=True)
	is_returned = fields.Boolean('Is Returned', default=True)
	is_invoice = fields.Boolean('Is Invoice', default=_get_default_inv_ref)




	def _get_communication(self, payment_method_id):
		return self.name or ''

	@api.multi
	def validate_referral(self, context):
		if self.invoice_id:
			payment_obj = self.env['account.payment']
			payment_methods = self.journal_id.inbound_payment_method_ids or self.journal_id.outbound_payment_method_ids
			currency = self.journal_id.company_id.currency_id
			# print(payment_methods)
			# pay = payment_obj.create({
			# 	'payment_method_id': payment_methods and [payment_methods[0].id] or False,
			# 	'payment_type': 'inbound',
			# 	'partner_type': 'customer',
			# 	'partner_id': self.invoice_id.partner_id.id,
			# 	'amount': abs(self.commission_amount),
			# 	'journal_id': self.journal_id.id,
			# 	'payment_date': fields.Date.today(),
			# 	'communication': self.invoice_id.number,
			# 	'invoice_ids': self.invoice_id.id,
			# 	'date': self.date,
			# 	'currency_id': currency.id,
			# 	'communication': self._get_communication(payment_methods[0] if payment_methods else False),
			# 	'name': self.name or _("Referral Commission %s") %  self.date,
			# 	})
			r_name = ''
			if self.name:
				r_name = self.name
			else:
				r_name = _("Referral Commission %s") %  self.date
				self.name = r_name
			query = """
			INSERT INTO "account_payment" 
			("id", "create_uid", "create_date", 
			"write_uid", "write_date", "amount", 
			"communication", "currency_id", "journal_id", 
			"move_name", "multi", "name", "partner_id", 
			"partner_type", "payment_date", 
			"payment_difference_handling", 
			"payment_method_id", "payment_type", 
			"state", "writeoff_label", "referral_payment_id","referral_id","ref_state") VALUES 
			(nextval('account_payment_id_seq'), 
			"""+str(self.env.uid)+""", (now() at time zone 'UTC'), """+str(self.env.uid)+""", 
			(now() at time zone 'UTC'), '"""+str(self.commission_amount)+"""', '"""+str(self.invoice_id.number)+"""', """+str(currency.id)+""", """+str(self.journal_id.id)+""", 
			NULL, false, '"""+str(r_name)+"""', 
			"""+str(self.partner_id.id)+""", 'customer', (now() at time zone 'UTC'), 'open', """+str(payment_methods[0].id)+""", 'inbound', 'draft', 'Write-Off', """+str(self.id)+""", """+str(self.partner_id.id)+""",'payment')RETURNING id
			"""
			created_payment = self._cr.execute(query)

			# Get the created object
			pay_id = payment_obj.search([('referral_payment_id', '=', self.id)])
			for single_pay in pay_id:
				single_pay.post()
			#Change the state
			self.is_validated = False
			self.is_invoice = False

	@api.multi
	def return_referral(self, context):
		if self.invoice_id:
			payment_obj = self.env['account.payment']
			payment_methods = self.journal_id.inbound_payment_method_ids or self.journal_id.outbound_payment_method_ids
			currency = self.journal_id.company_id.currency_id
			r_name = ''
			if self.name:
				r_name = self.name
			else:
				r_name = _("Refund Referral Commission %s") %  self.date
				self.name = r_name
			query = """
			INSERT INTO "account_payment" 
			("id", "create_uid", "create_date", 
			"write_uid", "write_date", "amount", 
			"communication", "currency_id", "journal_id", 
			"move_name", "multi", "name", "partner_id", 
			"partner_type", "payment_date", 
			"payment_difference_handling", 
			"payment_method_id", "payment_type", 
			"state", "writeoff_label", "referral_payment_id","referral_id","ref_state") VALUES 
			(nextval('account_payment_id_seq'), 
			"""+str(self.env.uid)+""", (now() at time zone 'UTC'), """+str(self.env.uid)+""", 
			(now() at time zone 'UTC'), '"""+str(self.commission_amount)+"""', '"""+str(self.invoice_id.number)+"""', """+str(currency.id)+""", """+str(self.journal_id.id)+""", 
			NULL, false, '"""+str(r_name)+"""', 
			"""+str(self.invoice_id.partner_id.id)+""", 'customer', (now() at time zone 'UTC'), 'open', """+str(payment_methods[0].id)+""", 'outbound', 'draft', 'Write-Off', """+str(self.id)+""", """+str(self.partner_id.id)+""",'refund')RETURNING id
			"""
			created_payment = self._cr.execute(query)

			# Get the created object
			pay_id = payment_obj.search([('referral_payment_id', '=', self.id),('payment_type', '=', 'outbound')])
			for single_pay in pay_id:
				single_pay.post()
			#Change the state
			self.is_returned = False
