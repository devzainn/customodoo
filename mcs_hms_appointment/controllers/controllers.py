# -*- coding: utf-8 -*-
# from odoo import http


# class McsHmsAppointment(http.Controller):
#     @http.route('/mcs_hms_appointment/mcs_hms_appointment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_hms_appointment/mcs_hms_appointment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_hms_appointment.listing', {
#             'root': '/mcs_hms_appointment/mcs_hms_appointment',
#             'objects': http.request.env['mcs_hms_appointment.mcs_hms_appointment'].search([]),
#         })

#     @http.route('/mcs_hms_appointment/mcs_hms_appointment/objects/<model("mcs_hms_appointment.mcs_hms_appointment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_hms_appointment.object', {
#             'object': obj
#         })
