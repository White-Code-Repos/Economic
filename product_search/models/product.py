# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################

from odoo import _, api, exceptions, fields, models, tools

class Product(models.Model):
    _inherit = 'product.template'

    serial_number = fields.Char(string="Serial Number")
    vendor_code = fields.Char(string="Vendor Code")
    exact_referance = fields.Char(string="Exact Refereance")