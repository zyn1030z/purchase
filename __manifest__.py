# -*- coding: utf-8 -*-
{
    'name': 'Purchase Request',
    'version': '1.0',
    'summary': 'Odoo 13 Purchase Request',
    'sequence': 1,
    'description': """""",
    'category': 'Tutorials',
    'author': 'Hung Pham',
    'maintainer': '',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'purchase',

    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/test.xml',
        'views/purchase_request.xml'
    ],
    'demo': [],
    'qweb': [],
    'images': [''],
    'installable': True,
    'application': True,
    'auto_install': False,
}
