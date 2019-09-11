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
    'name': 'Product Low Stock Notification "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Inventory',
    'summary': 'Get Notification of any product which reaches the minimum quantity',
    'description': """ 
        As a Manager you need to keep track of all products stock which reaches the minimum stock rule defined
        Steps:-
        1- Go to product and set the minimum quantity to get notified about
        2- A cron job will start to send a report daily about all products with minimum stock rule
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['base','product','mail'],
    'data': [
                'security/product_low_stock_notify_security.xml',
                'views/product_template.xml',
                'views/ir_cron.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':35.99,
    'currency':'EUR', 
}

