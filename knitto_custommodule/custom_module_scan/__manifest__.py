# -*- coding: utf-8 -*-
{
    'name': "Module Scan",

    'description': """
        Addons ini merupakan addons yang digunakan untuk melakukan proses scanning flow process pada Kartu Proses
    """,

    'author': "Adhitia Zain Nurrizki",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','tj_mkt_order','hr','web','tj_produksi'],

    'data': [
        'security/ir.model.access.csv',
        'static/src/xml/custom_module_scan_landing_page.xml',
        'static/src/xml/process_scanning.xml',
        'views/index_view.xml',
        # 'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}