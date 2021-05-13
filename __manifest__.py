# -*- coding: utf-8 -*-
{
    'name': 'Purchase Request',
    'version': '1.0',
    'sequence': 1,
    'summary': 'Odoo 14 Purchase Request',
    'description': """""",
    'category': 'Tutorials',
    'author': 'Hung Pham',
    'maintainer': '',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'purchase',
        'account'
    ],
    'data': [
        'security/purchase_request_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_request.xml',
        'views/reject_reason.xml',
        'views/asset.xml',
        'reports/purchase_request_template.xml',
        'reports/report.xml',
        'data/sequence.xml',
    ],
    'demo': [],
    'qweb': [],
    'images': [''],
    'installable': True,
    'auto_install': False,
    'application': True,

}
