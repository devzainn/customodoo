{
    "name" : "Work Order",
    "description" : "Work Order",
    "author" : "Samuel dan Adhitia Zain Nurrizki",
    "depends" : [
        'sale',
        'sale_contract',
        'tj_mkt_order',
    ],
    "data" : [
        # 'views/assets.xml',
        'views/color_kitchen.xml',
        'views/work_order.xml',
        'views/kp.xml',
        'views/sale_order_inherit_view.xml',
        # 'views/inherit_outstanding.xml',

        'wizard/wizard_create_kp.xml',
        'wizard/wizard_create_kp_wholesale.xml',
        'wizard/wizard_message.xml',
        'wizard/wizard_confirm_work_order_view.xml',
        'wizard/notulenWizard.xml',
        "wizard/work_order_rak_variasi_wizard_view.xml",
        'wizard/pop_up_warning.xml',
    ],
    "qweb": [
        'static/src/xml/header_tree.xml',
    ],
    "assets":{
        "web.assets_backend":[
            "/work_order/static/src/js/show_all_keterangan.js",
        ]
    }
}