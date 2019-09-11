# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from odoo import models, fields

class res_partner(models.Model):
    _inherit= 'res.partner'
    
    check_credit = fields.Boolean('Check Credit')
    credit_limit_on_hold  = fields.Boolean('Credit limit on hold')
    credit_limit = fields.Float('Credit Limit')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: