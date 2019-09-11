# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1
#
##############################################################################

from odoo import fields, models, api, _
from datetime import datetime

class backorder_reason(models.Model):
	_name = 'backorder.reason'

	name=fields.Char('Backorder Reason')
	description=fields.Text('Reason Description')
    
    

