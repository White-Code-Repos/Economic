# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class ProductCardReport(models.TransientModel):
    _name = 'product.card.report'
    _description = 'Product Card Report'

    product_id = fields.Many2one('product.product', string='Product')
    location_id = fields.Many2one('stock.location', domain="[('usage', '=', 'internal')]", string="Location")

    date = fields.Datetime('Inventory at Date', help="Choose a date to get the inventory at that date", default=fields.Datetime.now)
    default_code = fields.Char(string='Default Code')
    balance = fields.Float(string="Balance", compute='_compute_quantities',digits=dp.get_precision('Product Unit of Measure'),)
    def card_table(self):
        self.ensure_one()

        tree_view_id = self.env.ref('product_card_report.view_move_line_tree_inherot').id
        form_view_id = self.env.ref('product_card_report.view_move_line_form_inherot').id
        # We pass `to_date` in the context so that `qty_available` will be computed across
        # moves until date.
        action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': _('Product Moves'),
                'res_model': 'stock.move.line',
                'domain' : [('product_id','=', self.product_id.id),'|',('location_id','=',self.location_id.id),('location_dest_id','=',self.location_id.id)]
                # 'context': dict(search_default_done=1, search_default_product_id=self.product_id.id, search_default_location_id=self.location_id.id, | ,search_default_location_dest_id=self.location_id.id),
        }

        # tree_view_id = self.env.ref('stock.view_stock_product_tree').id
        # form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
        # # We pass `to_date` in the context so that `qty_available` will be computed across
        # # moves until date.
        # action = {
        #         'type': 'ir.actions.act_window',
        #         'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
        #         'view_mode': 'tree,form',
        #         'name': _('Products'),
        #         'res_model': 'product.product',
        #         'context': dict(self.env.context, to_date=self.date, default_id=self.product_id.id,),
        # }
        return action