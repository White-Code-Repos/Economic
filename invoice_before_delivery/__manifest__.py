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
    'name': 'Invoice Before Delivery "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Sales Management',
    'summary': 'this module will prevent the delivery order from being created until the invoice is validated',
    'description': """ 
        Some times you want to avoid creating of delivery order till invoice created from confirmed sale order,
        so that module will help you to achieve that, just follow this porcess
        1-Create sale order
        2- Select storable products and set qty and prices
        3-Confirm order "No delivery order created"
        4- Create invoice
        5- Vlidate invoice "New Button will appear in related sale order"
        6-Move to the sale order to create youur delivery order
       
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale', 'purchase', 'stock', 'account'],
    'data': [
        'views/sale_view.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':14.99,
    'currency':'EUR', 
}
