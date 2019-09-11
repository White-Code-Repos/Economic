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
    'name': 'Account Check Management',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Accounting Check Egypt',
    'author': 'Mostafa Abd El Fattah<mostafa.ic2@gmail.com>',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'account',
        # for bank and cash menu and also for better usability
        #'account_payment_fix',
    ],
    'data': [
        'data/account_payment_method_data.xml',

        'wizard/account_check_action_wizard_view.xml',
        'wizard/check_action_view_changes.xml',

        'views/account_payment_view.xml',
        'views/account_check_view.xml',
        'views/account_journal_dashboard_view.xml',
        'views/account_journal_view.xml',
        'views/account_checkbook_view.xml',
        'views/res_company_view.xml',
        'views/account_chart_template_view.xml',

        'security/ir.model.access.csv',
        'security/account_check_security.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
