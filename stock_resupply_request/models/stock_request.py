# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1  or Mobile: +201000925026
#
##############################################################################

from odoo import api, fields, models, _ , SUPERUSER_ID
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('inprogress', 'In Progress'),
    ('warehouse', 'Warehouse Operations'),
    ('rejected', 'Rejected'),
    ('done', 'Done')
]

class StockResupplyRequest(models.Model):

    _name = 'stock.resupply.request'
    _description = 'Stock Request Resupply'
    _inherit = ['mail.thread']

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code('stock.resupply.request')


    name = fields.Char('Request Code', size=32, required=True,
                       default=_get_default_name,
                       track_visibility='onchange')
    date_start = fields.Date('Start date',
                             help="Date when the user initiated the request.",
                             default=fields.Date.context_today,
                             track_visibility='onchange')
    end_start = fields.Date('End date',default=fields.Date.context_today,
                             track_visibility='onchange')
    requested_by = fields.Many2one('res.users',
                                   'Requested by',
                                   required=True,
                                   track_visibility='onchange',
                                   default=_get_default_requested_by)
    assigned_to = fields.Many2one('res.users', 'Approver', required=True,
                                  track_visibility='onchange')

    request_from = fields.Many2one('stock.location', 'Request From',domain=[('usage', '=', 'internal')], required=True)
    
    ship_to = fields.Many2one('stock.location', 'Ship To',domain=[('usage', '=', 'internal')], required=True)
    
    description = fields.Text('Description')

    line_ids = fields.One2many('stock.resupply.request.line', 'request_id',
                               'Products Needed',
                               readonly=False,
                               copy=True,
                               track_visibility='onchange')
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')


    @api.onchange('state')
    def onchange_state(self):
        assigned_to = None
        if self.state:
            if (self.requested_by.id == False):
                self.assigned_to = None
                return
        self.assigned_to =  assigned_to


    @api.one
    @api.depends('state')
    def _compute_inprogress(self):
        current_user_id = self.env.uid
        if(self.state == 'to_approve' and current_user_id == self.assigned_to.id):
            self.inprogress = True
        else:
            self.inprogress = False
    inprogress = fields.Boolean(string='In Progress',compute='_compute_inprogress' )


    @api.one
    @api.depends('state')
    def _compute_can_reject(self):
        self.can_reject = (self.inprogress)

    can_reject = fields.Boolean(string='Can reject',compute='_compute_can_reject')


    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ('to_approve', 'inprogress', 'rejected', 'done'):
                rec.is_editable = False
            else:
                rec.is_editable = True

    is_editable = fields.Boolean(string="Is editable",
                                 compute="_compute_is_editable",
                                 readonly=True)

    @api.multi
    def button_draft(self):
        self.mapped('line_ids').do_uncancel()
        return self.write({'state': 'draft'})

    @api.multi
    def button_to_approve(self):
        return self.write({'state': 'to_approve'})

    @api.multi
    def button_leader_approved(self):
        return self.write({'state': 'inprogress'})

    @api.multi
    def button_rejected(self):
        self.mapped('line_ids').do_cancel()
        return self.write({'state': 'rejected'})

    @api.multi
    def button_done(self):
        return self.write({'state': 'done'})

    @api.multi
    def check_auto_reject(self):
        """When all lines are cancelled the stock request should be
        auto-rejected."""
        for pr in self:
            if not pr.line_ids.filtered(lambda l: l.cancelled is False):
                pr.write({'state': 'rejected'})


    @api.multi
    def make_stock_request(self):
        order_line = []
        domain = [('view_location_id', 'parent_of', self.request_from.id)]
        warehouse_id =  self.env['stock.warehouse'].search(domain, limit=1)
        picking_type = self.env['stock.picking.type'].search([('warehouse_id', '=', warehouse_id.id),('code', '=', 'internal')])
        # picking_type = self.env['stock.picking.type'].search([('code','=','internal')])
        one2many_field = []
        for line in self.line_ids:
          product = line.product_id
          # pass one2many fields
          products_list = (0,0,{
          'product_id':line.product_id.id,
          'product_uom' : line.product_id.uom_id.id,
          'product_uom_qty':line.product_qty,
          'name': 'Stock Request Internal Transfer',
          'location_id': self.request_from.id,
          'location_dest_id': self.ship_to.id,
          })
          one2many_field.append(products_list)
        picking_obj = self.env['stock.picking']
        created_pick = picking_obj.create({
                'picking_type_id' : picking_type.id,
                'location_id' :self.request_from.id,
                'location_dest_id' :self.ship_to.id,
                'origin' :self.name,
                'note' :self.description,
                'move_lines' : one2many_field,
        })
        created_pick.action_confirm()
        self.write({'state': 'warehouse'})
          



class StockResupplyRequestLine(models.Model):

  _name = "stock.resupply.request.line"
  _description = "Stock Resupply Request Line"
  _inherit = ['mail.thread']

  @api.multi
  @api.depends('product_id', 'name', 'product_uom_id', 'product_qty',
                'date_required', 'notes')


  @api.multi
  def _compute_supplier_id(self):
      for rec in self:
          if rec.product_id:
              if rec.product_id.seller_ids:
                  rec.supplier_id = rec.product_id.seller_ids[0].name

  product_id = fields.Many2one(
      'product.product', 'Product',
      domain=[('purchase_ok', '=', True)], required=True,
      track_visibility='onchange')
  name = fields.Char('Description', size=256,
                     track_visibility='onchange')
  product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure',
                                   track_visibility='onchange')
  product_qty = fields.Float('Quantity', track_visibility='onchange',
                             digits=dp.get_precision(
                                 'Product Unit of Measure'))
  request_id = fields.Many2one('stock.resupply.request',
                               'Purchase Request',
                               ondelete='cascade', readonly=True)
  company_id = fields.Many2one('res.company',
                               string='Company',
                               store=True, readonly=True)

  requested_by = fields.Many2one('res.users',
                                 related='request_id.requested_by',
                                 string='Requested by',
                                 store=True, readonly=True)
  assigned_to = fields.Many2one('res.users',
                                related='request_id.assigned_to',
                                string='Assigned to',
                                store=True, readonly=True)
  date_start = fields.Date(related='request_id.date_start',
                           string='Request Date', readonly=True,
                           store=True)
  end_start = fields.Date(related='request_id.end_start',
                           string='End Date', readonly=True,
                           store=True)
  description = fields.Text(related='request_id.description',
                            string='Description', readonly=True,
                            store=True)
  date_required = fields.Date(string='Request Date', required=True,
                              track_visibility='onchange',
                              default=fields.Date.context_today)

  notes = fields.Text(string='Notes')
  request_state = fields.Selection(string='Request state',
                                   readonly=True,
                                   related='request_id.state',
                                   selection=_STATES,
                                   store=True)
  supplier_id = fields.Many2one('res.partner',
                                string='Preferred supplier',
                                compute="_compute_supplier_id")

  cancelled = fields.Boolean(
      string="Cancelled", readonly=True, default=False, copy=False)

  @api.onchange('product_id')
  def onchange_product_id(self):
      if self.product_id:
          name = self.product_id.name
          if self.product_id.code:
              name = '[%s] %s' % (name, self.product_id.code)
          if self.product_id.description_purchase:
              name += '\n' + self.product_id.description_purchase
          self.product_uom_id = self.product_id.uom_id.id
          self.product_qty = 1
          self.name = name

  @api.multi
  def do_cancel(self):
      """Actions to perform when cancelling a purchase request line."""
      self.write({'cancelled': True})

  @api.multi
  def do_uncancel(self):
      """Actions to perform when uncancelling a purchase request line."""
      self.write({'cancelled': False})

  def _compute_is_editable(self):
      for rec in self:
          if rec.request_id.state in ('to_approve', 'inprogress',  'rejected',
                                      'done'):
              rec.is_editable = False
          else:
              rec.is_editable = True

  is_editable = fields.Boolean(string='Is editable',
                               compute="_compute_is_editable",
                               readonly=True)
  @api.multi
  def write(self, vals):
      res = super(StockResupplyRequestLine, self).write(vals)
      if vals.get('cancelled'):
          requests = self.mapped('request_id')
          requests.check_auto_reject()
      return res
