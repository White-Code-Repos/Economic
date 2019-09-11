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
    'name': 'Back Order Notification YES/NO "Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Inventory',
    'summary': 'Get Notification of any backorder created or not created',
    'description': """ 
        As a Manager you need to keep track of all backOrders which created or orders proceed without backorder
        Steps:-
        1- Set Access rights for any user you want to get the notification
        2-Go to picking and recieve partially 
        3-Decide whether you want to create backorder or not
        4-An email will be sent to the selected users notify them about that backorder with a ling to redirect them back to the sysrtem
       
    """,
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>', 
    'website': 'https://www.linkedin.com/in/mabdelfattah1/',
    'images': ['images/main_screenshot.png'],
    'depends': ['base','sale', 'purchase', 'stock', 'account','mail'],
    'data': [
        'security/back_order_security.xml',
    ],
    'test': [],
    'installable':True,
    'application':True,
    'auto-install':False,
    'price':19.99,
    'currency':'EUR', 
}
