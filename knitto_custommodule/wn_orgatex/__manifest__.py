# -*- coding: utf-8 -*-
{
    'name': "Support Orgatex",
    'summary': 'Support Orgatex',
    'description': """
        Support Orgatex
    """,
    "license": "AGPL-3",
    'author': "Winaldi dan Adhitia Zain Nurrizki",
    'website': "https://aws.com",
    'category': 'extra',
    'version': '10.0.0.1',
    'depends': 
            [
                'base',
                'tj_mkt_order',
                'tj_stock',
                'tj_produksi',
            ],
    'data': [
                'security/ir.model.access.csv',
                'views/w_preference_master.xml',
                'views/w_labdip_warna.xml',
                'views/w_product_template.xml',
                # 'views/w_color_kitchen.xml',
                'views/archive.xml',
                'views/temporary.xml',
                'views/stock_move.xml',
                
                'report/w_color_kitchen_dyeing.xml',
            ],

    "application": True,
    "installable": True,
    "auto_install": False,
}
