# -*- coding: utf-8 -*-
# from odoo import http


# class McsHmsPatient(http.Controller):
#     @http.route('/mcs_hms_patient/mcs_hms_patient', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_hms_patient/mcs_hms_patient/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_hms_patient.listing', {
#             'root': '/mcs_hms_patient/mcs_hms_patient',
#             'objects': http.request.env['mcs_hms_patient.mcs_hms_patient'].search([]),
#         })

#     @http.route('/mcs_hms_patient/mcs_hms_patient/objects/<model("mcs_hms_patient.mcs_hms_patient"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_hms_patient.object', {
#             'object': obj
#         })
