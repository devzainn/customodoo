# -*- coding: utf-8 -*-
from odoo import http

# class TestingChallengeTree(http.Controller):
#     @http.route('/testing_challenge_tree/testing_challenge_tree/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/testing_challenge_tree/testing_challenge_tree/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('testing_challenge_tree.listing', {
#             'root': '/testing_challenge_tree/testing_challenge_tree',
#             'objects': http.request.env['testing_challenge_tree.testing_challenge_tree'].search([]),
#         })

#     @http.route('/testing_challenge_tree/testing_challenge_tree/objects/<model("testing_challenge_tree.testing_challenge_tree"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('testing_challenge_tree.object', {
#             'object': obj
#         })