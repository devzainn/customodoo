from odoo import fields, models, api


class DiagnosaGizi(models.Model):
    _name = 'master.diagnosa_gizi'

    kode = fields.Char('Kode')
    name = fields.Char('Masalah')
    deskripsi = fields.Text('Deskripsi')
