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
    'name': 'Sale Warehouse Branch"Community & Enterprise"',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Extra Tools',
    'summary': 'Add referral commisions in sale order or in invoice',
    'description': """ 
        > Seperate warehouses by users credentials and only require stock according to quotation
        from allowed warehoueses

    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.jpg'],
    'depends': ['base','sale','account','stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/sw_branch_secuirty.xml',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
}

