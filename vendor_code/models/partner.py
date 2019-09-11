# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from odoo import models, fields

class res_partner(models.Model):
    _inherit= 'res.partner'
    
    vendor_code = fields.Char(string="Vendor Code")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: