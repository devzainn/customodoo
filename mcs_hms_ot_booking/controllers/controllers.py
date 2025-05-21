# -*- coding: utf-8 -*-
# from odoo import http


# class McsHmsOtBooking(http.Controller):
#     @http.route('/mcs_hms_ot_booking/mcs_hms_ot_booking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_hms_ot_booking/mcs_hms_ot_booking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_hms_ot_booking.listing', {
#             'root': '/mcs_hms_ot_booking/mcs_hms_ot_booking',
#             'objects': http.request.env['mcs_hms_ot_booking.mcs_hms_ot_booking'].search([]),
#         })

#     @http.route('/mcs_hms_ot_booking/mcs_hms_ot_booking/objects/<model("mcs_hms_ot_booking.mcs_hms_ot_booking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_hms_ot_booking.object', {
#             'object': obj
#         })
