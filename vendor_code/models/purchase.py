from odoo import models, fields, api

class PurchaseOrderLines(models.Model):
    _inherit= 'purchase.order.line'
    
    vendor_code = fields.Char(string="Vendor Code")
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLines, self).onchange_product_id()
        if self.product_id.vendor_code == self.partner_id.vendor_code:
            self.vendor_code = self.product_id.vendor_code      	 