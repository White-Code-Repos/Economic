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
    'name': 'Taxed and Untaxed Journal Switcher "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Invoicing Management',
    'summary': 'Differentiate between the Taxed and Untaxed Journals Depinding the Fiscal Postion Configuration',
    'description': """ 
        Differentiate between the Taxed and Untaxed Journals Depinding the Fiscal Postion Configuration
        Steps:-
        1- Go To Define Fiscal Position with Tax & Account & Journal mapping.
        2- Create your invoice and select the desired fiscal position before adding any product
        3- you will got list of invoices with another journal from customer invoices.

        Note:- You Can Adjust related journal account - and leave tax empty in fiscal postion
        Updates #1
        1- Move the fiscal position on sale order under customer
        2- Make the account invoice affected by fiscal position in joural
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale', 'purchase', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/account_invoice_view.xml',
        'views/sale_view.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':9.99,
    'currency':'EUR', 
}
