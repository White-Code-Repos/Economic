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
    'name': 'Stock Resupply Request "Community & Enterprise"',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Inventory',
    'summary': 'Make A stock request and trace your request easily till done process',
    'description': """ 
        Make A stock requst through the module and keep track of your request,
        the warehouse manager will recieve your requst and will create internal transfer
        from the request.
        steps:-
        1- install module
        2- Grant user access whether request user or manager
        3- Go To Module 
        4-Create new stock request, set all the required data which is 
          (request from , ship to, products, quantities,......etc)
        5-Set Approval user of your request who will proceed with the request
        6-As Approval, Set request in progress and create Transfer from request
        7-A new transfer will be automatically created in the related location set
        8-Proceed with the transfer
        9-Set the request To Done            

    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.jpg'],
    'depends': ['base','sale','mail','stock'],
    'data': [
        'data/stock_resupply_request_data.xml',
        'security/stock_resupply_request_security.xml',
        'security/ir.model.access.csv',
        'views/stock_resupply_request_view.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':45,
    'currency':'EUR', 
}

