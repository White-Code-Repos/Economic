# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import Counter

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools.pycompat import izip
from odoo.tools.float_utils import float_round, float_compare, float_is_zero


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # @api.multi
    # @api.depends('qty_done')
    # def _compute_quantities(self):
    # 	for obj in self:
    #         if obj.product_id:
    #             print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    #             print("qty available: ", obj.product_id.qty_available)
    #             print("qty done: ",obj.qty_done)
    #             obj.balance_move_loc = obj.product_id.qty_available - obj.qty_done
    #             obj.balance_move_desto = obj.product_id.qty_available + obj.qty_done
    #             print("loc qty: ",obj.balance_move_loc)
    #             print("dest qty: ",obj.balance_move_desto)

    @api.model
    def create(self,vals):
        res = super(StockMoveLine, self).create(vals)
        if 'product_id' in vals: 
            product = self.env['product.template'].browse(vals['product_id'])
            print("9999999999999999999999999999")
            print(product)
#            print(product.qty_available)
     #       balance_move_loc = product.qty_available
           # res.update({'balance_move_loc':balance_move_loc})
        return res

    balance_move_loc=fields.Float(string="Balance",digits=dp.get_precision('Product Unit of Measure'))
    balance_move_desto=fields.Float(string="Balance" ,digits=dp.get_precision('Product Unit of Measure'))
    
    def _action_done(self):

        res = super(StockMoveLine,self)._action_done()
 #       self.update({'balance_move_loc':self.product_id.qty_available})
        return res 

	# @api.onchange('qty_done','')
 #    @api.one
 #    def _onchange_qty_done(self):
 #        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
 #        print("qty available: ", self.product_id.qty_available)
 #        print("qty done: ",self.qty_done)
 #        balance_move_loc = self.product_id.qty_available - self.qty_done
 #        balance_move_desto = self.product_id.qty_available + self.qty_done
 #        print("loc qty: ",self.balance_move_loc)
 #        print("dest qty: ",self.balance_move_desto)
 #        self.write({'balance_move_loc',balance_move_loc,
 #             'balance_move_desto',balance_move_desto,
 #        	})
