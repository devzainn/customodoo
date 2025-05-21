from odoo import api, fields, models


class InheritPhysician(models.Model):
    _inherit = 'hms.physician'

    peran = fields.Selection([
        ('dokter', 'Dokter'),
        ('perawat', 'Perawat'),
        ('apoteker', 'Apoteker'),
    ], string='Peran', default='dokter')