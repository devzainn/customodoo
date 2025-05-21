from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NamaModel(models.Model):
    _inherit = 'stock.move'

    tahapan = fields.Char('Tahapan', )
    # tahapan = fields.Selection(
    #     selection=[
    #         ('#OPC 01', 'TAHAP 01'),
    #         ('#OPC 02', 'TAHAP 02'),
    #         ('#OPC 03', 'TAHAP 03'),
    #         ('#OPC 04', 'TAHAP 04'),
    #         ('#OPC 05', 'TAHAP 05'),
    #         ],
    #     string='Tahap', default="#OPC 01", )

    