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
from odoo.tools.float_utils import float_compare

class StockBackorderConfirmation(models.TransientModel):
  _inherit = 'stock.backorder.confirmation'


  @api.one
  def _process(self, cancel_backorder=False):
    if cancel_backorder:
      for pick_id in self.pick_ids:
        moves_to_log = {}
        for move in pick_id.move_lines:
          if float_compare(move.product_uom_qty, move.quantity_done, precision_rounding=move.product_uom.rounding) > 0:
            moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
            pick_id._log_less_quantities_than_expected(moves_to_log)
    self.pick_ids.action_done()
    if cancel_backorder==False:
      backorder_pick = {}
      for pick_id in self.pick_ids:
        backorder_pick = self.env['stock.picking'].search([('backorder_id', '=', pick_id.id)])
      if backorder_pick:
        self.send_notification_backorder(backorder_pick,cancel_backorder=False)
    if cancel_backorder:
      backorder_pick = {}
      for pick_id in self.pick_ids:
        backorder_pick = self.env['stock.picking'].search([('backorder_id', '=', pick_id.id)])
        backorder_pick.action_cancel()
        pick_id.message_post(body=_("Back order <em>%s</em> <b>cancelled</b>.") % (backorder_pick.name))
      self.send_notification_backorder(backorder_pick,cancel_backorder=True)


  def send_notification_backorder(self,backorder_pick,cancel_backorder):
    for pick_id in self.pick_ids:

      group_backorder_notification = self.env.ref('backorder_yes_no_notification.back_order_security')

      partnerz = [u.partner_id.id for u in group_backorder_notification.users]
      model_description = self.env['ir.model']._get(pick_id._name).display_name
      mail_obj = self.env['mail.thread']

      if partnerz:
        for part in partnerz:
          if cancel_backorder == False:
            message1="<p style='margin: 0px;'>\
                            <span>Dear "+self.env['res.partner'].search([('id', '=', part)]).name+",</span><br/>\
                            <span style='margin-top: 8px;'>Please note that a backorder has been created for picking "+pick_id.name+".</span>\
                            </p>\
                            <p style='margin-top: 24px; margin-bottom: 16px;'>\
                            <a style='background-color:#875A7B; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px;' href='/mail/view?model="+pick_id._name+"&amp;res_id="+str(pick_id.id)+"'>\
                              View Original Order\
                            </a>\
                            </p>\
                            <p style='margin: 0px;'>\
                            <span style='margin-top: 8px;'>Backorder name: "+backorder_pick.name+".</span>\
                            </p>\
                            <p style='margin-top: 24px; margin-bottom: 16px;'>\
                            <a style='background-color:#FF0000; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px;' href='/mail/view?model="+pick_id._name+"&amp;res_id="+str(backorder_pick.id)+"'>\
                              View BackOrder\
                            </a>\
                            </p>"
          else:
            message1="<p style='margin: 0px;'>\
                            <span>Dear "+self.env['res.partner'].search([('id', '=', part)]).name+",</span><br/>\
                            <span style='margin-top: 8px;'>Please note that Picking "+pick_id.name+" has been Validated with quantity done less than the ordered, with NO BackOrder.</span>\
                            </p>\
                            <p style='margin-top: 24px; margin-bottom: 16px;'>\
                            <a style='background-color:#875A7B; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px;' href='/mail/view?model="+pick_id._name+"&amp;res_id="+str(pick_id.id)+"'>\
                              View Order\
                            </a>\
                            </p>"

          assignation_msg = self.env['mail.thread']._replace_local_links(message1)
          mail_obj.message_notify(
                    subject=_('Backorder Notification'),
                    body=assignation_msg,
                    partner_ids=[(4, pid) for pid in [part]],
                    record_name=pick_id.name,
                    notif_layout='mail.mail_notification_light',
                    model_description=model_description,
                    )