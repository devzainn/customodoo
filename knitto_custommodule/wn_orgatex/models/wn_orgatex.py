from odoo import models, fields, api, _

class WnOrgatex(models.Model):
    _name = 'wn.orgatex'
    _description = 'WN Orgatex Table'
    _rec_name = 'product_name'

    no_program = fields.Char('Tahapan')
    batch_ref = fields.Char('Batch Ref')
    product_name = fields.Char(string="Product Name")
    qty_receipt = fields.Float(string="Quantity Receipt", digits=(16, 5))
    source_id = fields.Many2one('color.kitchen.dyeing', string="Source Dyeing")  
    proses_id = fields.Many2one('master.proses', string="Process")

    no_kartu_proses = fields.Char('No Kartu Proses')
    preparation_number = fields.Char('Preparation Number')
    no_obat_kp = fields.Char('No Obat KP')
    kode_chemical = fields.Char('Kode Chemical')
    nama = fields.Char('Nama')
    jenis_chemical = fields.Char('Jenis Chemical')
    toleransi = fields.Char('Toleransi Timbangan')
    kebutuhan = fields.Char('Kebutuhan')