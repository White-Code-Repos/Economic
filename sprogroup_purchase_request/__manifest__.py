# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Request',
    'version': '1.0',
    'category': 'Purchases',
    'author':'tung.tung11191@gmail.com',
    'description': """
Use Purchase Request module for requesting product.
    """,
    'summary': 'Create purchase request',
    'website': 'https://www.odoo.com/page/survey',
    'images': ['static/description/icon.jpg'],
    'depends': ['mail'],
    'data': [
        'data/sprogroup_purchase_request_data.xml',
        'security/sprogroup_purchase_request_security.xml',
        'security/ir.model.access.csv',
        'views/sprogroup_purchase_request_view.xml',
    ],
    'depends': ['hr'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 105,
    'license': 'AGPL-3',
}
