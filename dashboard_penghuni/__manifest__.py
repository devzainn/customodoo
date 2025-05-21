# -*- coding: utf-8 -*-
{
    'name': "dashboard_penghuni",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Adhitia Zain Nurrizki",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base','account','stock','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/inherit_auth.xml',
        'views/inherit_view.xml',
        # 'views/menu_dashboard.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'dashboard_penghuni/static/src/js/dashboard_penghuni.js',
    #         'dashboard_penghuni/static/src/js/dashboard_new.js',
    #         'dashboard_penghuni/static/src/js/penghuni_dashboard_service.js',
    #         'dashboard_penghuni/static/src/css/dashboard.css',
    #     ],
    #     'web.assets_qweb': [
    #         'dashboard_penghuni/static/src/xml/dashboard_penghuni.xml',
    #     ],
    # },

    'demo': [
        'demo/demo.xml',
    ],
}

