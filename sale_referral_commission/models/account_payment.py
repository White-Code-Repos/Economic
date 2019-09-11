# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

from itertools import groupby


class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    referral_payment_id = fields.Many2one('referral.commission', string="Referral Payment")
    referral_id = fields.Many2one('res.partner', string="Referral Person")
    ref_state = fields.Selection([('payment','Payment'),('refund','Refund')])