# -*- coding: utf-8 -*-
{
    'name': "mcs_hms_appointment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Adhitia Zain Nurrizki",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','acs_hms', 'acs_hms_base', 'acs_hms_laboratory', 'acs_hms_vital_examination'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',

        'data/cppt_input_column.xml',

        'reports/kartu_pasien.xml',
        'reports/surat_keterangan_sehat.xml',
        'reports/surat_klaim_rawat_jalan.xml',
        'reports/surat_rekomendasi_dpjp.xml',
        'reports/surat_kontrol_rawat_jalan.xml',
        'reports/appointment_report.xml',
        'reports/surat_bukti_pelayanan_bpjs.xml',
        'wizard/cancel_reason_view.xml',
        'views/appointment.xml',
        'views/master_data.xml',
        'views/master_diagnosis.xml',
        'views/master_encounter_class.xml',
        'views/master_status_observation.xml',
        # 'views/vital_template.xml',
        'views/templates.xml',
        'views/diseases.xml',
        'views/md_gizi.xml',
        'views/md_diagnosis_keperawatan_kategori.xml',
        'views/hms_physician.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
