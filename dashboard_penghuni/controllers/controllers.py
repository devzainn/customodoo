# -*- coding: utf-8 -*-
import logging
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http
from odoo.http import request
from collections import defaultdict
import json

_logger = logging.getLogger(__name__)

# class DashboardPenghuni(http.Controller):
    # @http.route('/dashboard_penghuni', type='http', auth='user', website=True)
    # def dashboard_penghuni(self):
    #     # Data dummy (ganti dengan data nyata sesuai kebutuhan)
    #     produk_pengeluaran = [
    #         {'label': 'Air', 'value': 500},
    #         {'label': 'Listrik', 'value': 300},
    #     ]
    #     produk_usage = [
    #         {'label': 'Air', 'value': 50},
    #         {'label': 'Listrik', 'value': 20},
    #     ]

    #     qcontext = {
    #         'produk_pengeluaran': produk_pengeluaran,
    #         'produk_usage': produk_usage,
    #     }

        # return request.render('dashboard_penghuni.ChartVisualization', qcontext)

# class DashboardController(http.Controller):
#     @http.route('/dashboard/data', type='json', auth='user')
#     def get_dashboard_data(self):
#         return request.env['dashboard.penghuni'].get_dashboard_data()

# class DashboardPenghuni(http.Controller):

    # @http.route('/dashboard', type='json', auth='user', website=True)
    # def dashboard(self, **kwargs):
    #     user = request.env.user
    #     partner_id = user.partner_id

    #     tagihan_records = request.env['dashboard.penghuni'].search([('partner_id', '=', partner_id.id)])

    #     produk_pengeluaran = defaultdict(float)
    #     for tagihan in tagihan_records:
    #         produk_pengeluaran[tagihan.layanan_id.name] += tagihan.invoice_id.amount_total

    #     _logger.info("Produk Pengeluaran: %s", produk_pengeluaran)

    #     produk_usage = defaultdict(int)
    #     for tagihan in tagihan_records:
    #         produk_usage[tagihan.layanan_id.name] += 1

    #     _logger.info("Produk Yang Digunakan: %s", produk_usage)

    #     active_tagihan = [
    #         {
    #             'produk': tagihan.layanan_id.name,
    #             'tanggal_tagihan': tagihan.tanggal_tagihan.strftime('%Y-%m-%d'),
    #             'status_pembayaran': tagihan.status_pembayaran
    #         } for tagihan in tagihan_records.filtered(lambda t: t.status_pembayaran == 'not_paid')
    #     ]

    #     paid_tagihan = [
    #         {
    #             'produk': tagihan.layanan_id.name,
    #             'tanggal_tagihan': tagihan.tanggal_tagihan.strftime('%Y-%m-%d'),
    #             'status_pembayaran': tagihan.status_pembayaran
    #         } for tagihan in tagihan_records.filtered(lambda t: t.status_pembayaran == 'paid')
    #     ]

    #     payment_history = []
    #     for tagihan in tagihan_records:
    #         for line in tagihan.invoice_id.payment_ids:
    #             payment_history.append({
    #                 'tanggal': line.payment_date.strftime('%Y-%m-%d'),
    #                 'jumlah': line.amount,
    #                 'produk': tagihan.layanan_id.name,
    #             })
                
    #     _logger.info("Produk Pengeluaran JSON: %s", json.dumps(dict(produk_pengeluaran)))
    #     _logger.info("Produk Usage JSON: %s", json.dumps(dict(produk_usage)))

    #     return {
    #         'produk_pengeluaran': dict(produk_pengeluaran),
    #         'produk_usage': dict(produk_usage),
    #         'active_tagihan': active_tagihan,
    #         'paid_tagihan': paid_tagihan,
    #         'payment_history': payment_history,
    #     }


    # @http.route('/dashboard/data', type='json', auth='user')
    # def get_dashboard_data(self):
    #     user = request.env.user
    #     partner_id = user.partner_id

    #     tagihan_records = request.env['dashboard.penghuni'].search([('partner_id', '=', partner_id.id)])
        
    #     produk_pengeluaran = defaultdict(float)
    #     for tagihan in tagihan_records:
    #         produk_pengeluaran[tagihan.layanan_id.name] += tagihan.invoice_id.amount_total

    #     produk_usage = defaultdict(int)
    #     for tagihan in tagihan_records:
    #         produk_usage[tagihan.layanan_id.name] += 1

    #     active_tagihan = [
    #         {
    #             'produk': tagihan.layanan_id.name,
    #             'tanggal_tagihan': tagihan.tanggal_tagihan,
    #             'status_pembayaran': tagihan.status_pembayaran
    #         } for tagihan in tagihan_records.filtered(lambda t: t.status_pembayaran == 'not_paid')
    #     ]

    #     paid_tagihan = [
    #         {
    #             'produk': tagihan.layanan_id.name,
    #             'tanggal_tagihan': tagihan.tanggal_tagihan,
    #             'status_pembayaran': tagihan.status_pembayaran
    #         } for tagihan in tagihan_records.filtered(lambda t: t.status_pembayaran == 'paid')
    #     ]

    #     payment_history = []
    #     for tagihan in tagihan_records:
    #         for line in tagihan.invoice_id.payment_ids:
    #             payment_history.append({
    #                 'tanggal': line.payment_date,
    #                 'jumlah': line.amount,
    #                 'produk': tagihan.layanan_id.name,
    #             })

    #     return {
    #         'produk_pengeluaran': dict(produk_pengeluaran),
    #         'produk_usage': dict(produk_usage),
    #         'active_tagihan': active_tagihan,
    #         'paid_tagihan': paid_tagihan,
    #         'payment_history': payment_history,
    #     }

class PenghuniDashboardController(http.Controller):
    @http.route('/penghuni_dashboard/get_data', type='json', auth='user')
    def get_data(self):
        partner_id = request.env.user.partner_id
        if not partner_id:
            return {}
        
        tagihan_records = request.env['dashboard.penghuni']._get_tagihan_data(partner_id)
        dashboard_data = request.env['dashboard.penghuni']._create_dashboard_data(tagihan_records)
        return dashboard_data

class CustomAuthSignup(http.Controller):

    @http.route('/web/signup', type='http', auth='public', website=True, csrf=False)
    def web_auth_signup(self, **kwargs):
        """Handle user signup with kode_rumah."""
        kode_rumah = kwargs.get('kode_rumah')

        if not kode_rumah:
            return request.render('dashboard_penghuni.auth_signup_form', {
                'error': 'Kode Rumah harus diisi.'
            })

        try:
            request.env['res.users'].sudo().signup({
                'login': kwargs.get('login'),
                'name': kwargs.get('name'),
                'password': kwargs.get('password'),
            })

            user = request.env['res.users'].sudo().search([('login', '=', kwargs.get('login'))], limit=1)
            if user:
                user.partner_id.sudo().write({'kode_rumah': kode_rumah})

            return request.redirect('/web/login')
        except UserError as e:
            return request.render('dashboard_penghuni.auth_signup_form', {
                'error': str(e),
            })

class CustomAuthLogin(http.Controller):

    @http.route('/web/login', type='http', auth='public', website=True, csrf=False)
    def web_login(self, **kwargs):
        """Custom login logic with kode_rumah for regular users."""
        login = kwargs.get('login')
        password = kwargs.get('password')
        kode_rumah = kwargs.get('kode_rumah')

        if not (login and password):
            return request.render('dashboard_penghuni.auth_login_form', {
                'error': 'Email dan Password harus diisi.'
            })

        try:
            request.session.authenticate(request.env.cr.dbname, login, password)
            user = request.env.user

            if user.has_group('base.group_system'):  
                return request.redirect('/web')

            if not user.partner_id.kode_rumah or user.partner_id.kode_rumah != kode_rumah:
                request.session.logout()
                return request.render('dashboard_penghuni.auth_login_form', {
                    'error': 'Kode Rumah salah atau tidak ditemukan.'
                })

            return request.redirect('/dashboard')

        except AccessDenied:
            return request.render('dashboard_penghuni.auth_login_form', {
                'error': 'Login gagal. Periksa Email, Password, atau Kode Rumah Anda.'
            })