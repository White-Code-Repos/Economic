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
    'name': 'Search By Partner Phone in other Modules "Community & Enterprise"',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Extra Tools',
    'summary': 'Search by Phone/Mobile Number on any Module related to Partner',
    'description': """ 
        Make it easy for you to search by customer phone or mobile number on any module related to  partner

    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.jpg'],
    'depends': ['base','sale'],
    'data': [
                'views/sale_views.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':15,
    'currency':'EUR', 
}

