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
    'name': 'Product Search "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Inventory',
    'summary': 'Search by more than one factor for product',
    'description': """ 
        Search with more than one factor in product list view
        1-Exact Internal Referanc
        2-Serial Number
        3- Vendor Code
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['base','product','mail'],
    'data': [
                'views/product_template.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
}

