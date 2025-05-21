{
    'name'          : "Knitto API", # isi bebas
    'version'       : "10.0.2.0.0",
    'summary'       : """Komunikasi dengan Aplikasi Knitto""",
   
    "depends": [
        "base",
        "sale_contract",
        "sale",
    ], 
    'author'        : "Winaldi dan Adhitia Zain Nurrizki",
    'company'       : "AWS",
    'website'       : "http://www.aws.com",
    'category'      : "Application",
    'data'          :   [
                        "views/kat_po_view.xml",
                        ],
    'license'       : "AGPL-3", # pilih antara GPL-2, GPL-3, AGPL-3, LGPL-3, OEEL-1, OPL-1, atau Other proprietary
    'installable'   : True, # harus True
    'auto_install'  : False,
    'application'   : True,
    'description'   : """

                    Media Komunikasi dengan Aplikasi Knitto

                    """,
    'images'        :["static/description/api.png"],
    'demo'          :[],
    'test'          :[],
}