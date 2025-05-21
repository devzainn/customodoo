from odoo import models, fields, api,_
class WizardMessage(models.TransientModel):
    _name = 'wizard.message'

    message = fields.Text('Message', required=True)

    @api.multi
    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}