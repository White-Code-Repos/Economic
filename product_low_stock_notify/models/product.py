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
from werkzeug import url_encode
from werkzeug import urls
import email
from email.message import Message
from datetime import date
import io
import base64

class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Notify manager for Qty Below',
                                          help='Set to -1 to exclude from the report.')

    @api.multi
    def send_low_stock_via_email(self):

        group_product_low_stock_notification = self.env.ref('product_low_stock_notify.product_low_stock_notify_security')
        partnerz = [u.partner_id.id for u in group_product_low_stock_notification.users]
        model_description = self.env['ir.model']._get(self._name).display_name
        mail_obj = self.env['mail.thread']

        header_label_list=["Code", "Name", "Qty On Hand","Forecasted Qty","Low Stock Qty","Product Review"]

        if partnerz:
            for part in partnerz:
                custom_body="<p style='margin: 0px;'>\
                            <span>Dear "+self.env['res.partner'].search([('id', '=', part)]).name+",</span><br/>\
                            <span style='margin-top: 8px;'>Please be informed about the below table of all products in your stock which less the minimum stock defined.</span>\
                            </p>"

                custom_body += """
                        <table style='border: 1px solid black; border-collapse: collapse;'>
                          <thead>
                            <tr>
                                <th style='border-collapse: collapse; border: 1px solid black; padding: 10px; background-color: black; color: white;'>%s</th>
                                <th style='border-collapse: collapse; border: 1px solid black; padding: 10px; background-color: black; color: white;'>%s</th>
                                <th style="border-collapse: collapse; border: 1px solid black; padding: 10px; text-align:center; background-color: black; color: white;">%s</th>
                                <th style="border-collapse: collapse; border: 1px solid black; padding: 10px; text-align:center; background-color: black; color: white;">%s</th>
                                <th style="border-collapse: collapse; border: 1px solid black; padding: 10px; text-align:center; background-color: black; color: white;">%s</th>
                                <th style="border-collapse: collapse; border: 1px solid black; padding: 10px; text-align:center; background-color: black; color: white;">%s</th>
                            </tr>
                           </thead>
                        """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4], header_label_list[5])
                
                ## Check for low stock products
                product_obj  = self.env['product.product']
                product_ids  = product_obj.search([('active', '=', True), ('sale_ok', '=', True)])
                for product in product_ids:
                    product_sku = product.default_code
                    # Check Quantity Available
                    qty_available = product.qty_available
                    qty_incoming  = product.virtual_available
                    qty_low_stock_notify = product.qty_low_stock_notify

                    if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0:
                        custom_body += """
                                        <tr style="font-size:10px;">
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">%s</td>
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">%s</td>
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">%s</td>
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">%s</td>
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">%s</td>
                                        <td style="padding: 10px; border-collapse: collapse; border: 1px solid black; text-align:center;">
                                        <p style='margin-top: 24px; margin-bottom: 16px;'>
                                        <a style='background-color:#875A7B; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px;' href='/mail/view?model=%s&amp;res_id=%s'>
                                             View Product
                                        </a>
                                        </p>

                                        </td>
                                        </tr>
                        """ %(product_sku, product.name, str(qty_available), str(qty_incoming), str(qty_low_stock_notify), product._name, str(product.id))
                        print(custom_body)
                custom_body  += "</table>"
                assignation_msg = self.env['mail.thread']._replace_local_links(custom_body)
                mail_obj.message_notify(
                        subject='Product Low Stock Report',
                        body=assignation_msg,
                        partner_ids=[(4, pid) for pid in [part]],
                        record_name=self.display_name,
                        notif_layout='mail.mail_notification_light',
                        model_description=model_description,
                        )