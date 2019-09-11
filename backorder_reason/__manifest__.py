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
    'name': 'Back Order Reason "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Inventory',
    'summary': 'Keep track of all backorder reasons',
    'description': """ 
            Fill in reason while creating backorders    
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_backorder_confirmation_views.xml',
        'views/stock_picking_views.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':8.99,
    'currency':'EUR', 
}