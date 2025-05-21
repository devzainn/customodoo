from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = "hms.consumable.line"

    price_unit = fields.Float(related=False, readonly=False)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else:
            self.price_unit = 0
