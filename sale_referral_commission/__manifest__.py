# -*- coding: utf-8 -*-
{
    'name': 'Referral Commissions Community & Enterprise',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Generic Modules/Sales Management',
    'summary': 'Add referral commisions in sale order or in invoice',
    'author': 'Mostafa Abd El Fattah mostafa.ic2@gmail.com',
    'depends': ['base','sale','mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/sale_view.xml',
        #'views/sale_config_setting.xml',
        'views/account_payment_view.xml',
        'views/account_commission_view.xml',
    ],
    'installable':True,
    'application':True,
    'auto-install':False,
}
