# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError,UserError,Warning

class mcs_hms_ot_booking(models.Model):
    _inherit = 'acs.ot.booking'

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')
    ot_id = fields.Many2one(required=False)


class McsinheritOTAppointment(models.Model):
    _inherit = 'hms.appointment'

    ot_count = fields.Integer(string='OT Booking', compute='_get_count_ot')


    def _get_count_ot(self):
        search_ot = self.env['acs.ot.booking'].sudo().search_count([('appointment_id','=',self.id)])
        if search_ot:
            self.ot_count = search_ot

        else:
            self.ot_count = 0

    def action_view_ot(self):
        ot_records = self.env['acs.ot.booking'].sudo().search([('appointment_id', '=', self.id)])
        if ot_records:
            action = self.env.ref('acs_hms_operation_theater.action_acs_ot_booking').read()[0]
            action['domain'] = [('id', 'in', ot_records.ids)]
            return action
        else:
            raise ValidationError(_('No OT records found!'))
