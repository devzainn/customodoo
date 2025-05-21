from odoo import api, fields, models


class McsRsDiagnosisKeperawatanKategori(models.Model):
    _name = 'master.diagnosis_keperawatan_kategori'
    _description = 'Diagnosis Keperawatan Kategori'
    _rec_name = 'name'
    
    name = fields.Char(string='Name')