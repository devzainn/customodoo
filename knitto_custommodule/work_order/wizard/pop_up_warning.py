from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PopUpWarning(models.TransientModel):
    _name = 'pop.up.warning'

    name = fields.Char(string='Label dari Field')


    @api.multi
    def set_open(self):
        context = self.env.context
        print 'set_open'
        print context
        tdId = context.get('td_id')
        wo_id = context.get('active_id') 
        woObj = self.env['sale.order'].browse(wo_id)
        # woObj.browse(wo_id).write({
        #     'hanger_code' : False,
        # })
        print(context)
        print(woObj.hanger_code.id)
        # absdajsda
        if woObj.hanger_code.id:
            view_id = self.env.ref('tj_mkt_order.tj_master_lot_form').id  
            mlotId = self.env['test.development'].browse(woObj.hanger_code.id).mlot_id.id
            # action = self.env.ref('tj_mkt_order.master_lot_action_draft').read()[0]
            action = {
                    'name': _('Mlot'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'test.development',
                    'views': [(view_id, 'form')],
                    'view_id': view_id,
                    # 'target': 'new',
                    'context' : {'wo_id' : wo_id},
                    'res_id': mlotId
                }
            return action