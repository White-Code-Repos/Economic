# -*- coding: utf-8 -*-

{
    'name': 'Purchase Request',
    'version': '1.0',
    'summary': 'Purchase Request',
    'author': 'Srikesh Infotech',
    'license': "AGPL-3",
    'website': 'http://www.srikeshinfotech.com',
    'description': """
        This module helps to create Pruchase Request.
    """,
    'price': 5,
    'currency': 'EUR',
    'images': ['images/main_screenshot.png'],
    'category': "Purchase Management",
    'depends': ['purchase'],

    "data": [
        "security/purchase_request.xml",
        "security/ir.model.access.csv",
        "data/purchase_request_seq.xml",
        "data/purchase_request_demo_data.xml",
        "views/purchase_request_view.xml",
        "reports/report_purchaserequests.xml",
        "views/purchase_request_report.xml",
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
