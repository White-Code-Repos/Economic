# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Laxicon Solution.
#    (<http://laxicon.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################


{
    'name': 'Purchase Order Discount',
    'version': '11.0',
    'category': 'purchase',
    'sequence': 9,
    'summary': 'Purchase Order line Discount',
    'description': """
    this module work for purchase order discount same as sale order line discount"
    """,
    'author': "Laxicon Solution",
    'website': "http://laxicon.in",
    'depends': [
        'purchase', 'account'
    ],
    'data': [
        'security/purchase_security.xml',
        'view/account_invoice.xml',
        'view/purchase_discount_view.xml'
            ],
    "images": [
        'static/description/icon.png'
    ],
    'demo': [],
    'price': 0,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}
