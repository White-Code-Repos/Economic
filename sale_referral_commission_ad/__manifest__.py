# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Mostafa Abd El Fattah ERP Consultant (<mostafa.ic2@gmail.com>).
#
#    For Module Support : mostafa.ic2@gmail.com  or Skype : mostafa.abd.elfattah1
#
##############################################################################
{
    'name': 'Referral Commissions Adjusted "Community & Enterprise"',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Sale',
    'summary': 'Add referral commisions in sale order or in invoice',
    'description': """
        Make it easy for you and your referral to handle all his/her commission
        from odoo.
         Install the module
         create sale order
         create a commission value
         confirm orer
         create invoice
         validate the invoice
         register the payment
         add the referral commission
         validate the commission
         trace the payment whether normal invoice or refund.

    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>',
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.jpg'],
    'depends': ['base','sale','mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/sale_view.xml',
        'views/sale_config_setting.xml',
        'views/account_payment_view.xml',
        'views/account_commission_view.xml'
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':45,
    'currency':'EUR',
}
