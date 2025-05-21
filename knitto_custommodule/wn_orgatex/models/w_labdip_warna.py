from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

class LabdipResepInherit(models.Model):
    _inherit = 'labdip.test.resep.line'

    toleransi   = fields.Float(string='Toleransi', digits=(16, 2), store=True,)
    tahapan     = fields.Many2one('wn.preference.master', string='Tahapan',)

class LabdipWarnaInherit(models.Model):
    _inherit = 'labdip.resep'

    toleransi   = fields.Float(string='Toleransi', digits=(16, 2), store=True,)
    tahapan     = fields.Many2one('wn.preference.master', string='Tahapan', store=True,)

class MasterProdukInherit(models.Model):
    _inherit = 'product.template'

    toleransi_timbang = fields.Float(string='Toleransi Timbang', digits=(16, 2), store=True,)


class ColorKitchenDyeing(models.Model):
    _inherit = 'color.kitchen.dyeing'


    @api.multi
    def print_resep_grouping(self):
        self.write({'status_print':True})
        return self.env['report'].get_action(self, 'wn_orgatex.color_kitchen_dyeing_template_group')


class ColorKitchenDyeingLine(models.Model):
    _inherit = 'color.kitchen.dyeing.line'

    toleransi_timbang = fields.Float(string='Toleransi Timbang', digits=(16, 2), store=True,)
    tahapan     = fields.Many2one('wn.preference.master', string='Tahapan', store=True,)
