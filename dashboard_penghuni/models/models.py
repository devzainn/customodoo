# -*- coding: utf-8 -*-
from odoo import models, fields, api

from datetime import timedelta

class DashboardData(models.Model):
    _name = 'dashboard.penghuni'
    _description = 'Data Tagihan Penghuni'
    _rec_name = 'partner_id'

    _access_rights = {
        'read': ['base.group_portal'],
    }

    partner_id = fields.Many2one('res.partner', string='Masyarakat', required=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    layanan_id = fields.Many2one('product.product', string='Layanan Digunakan', required=True)
    status_pembayaran = fields.Selection(related='invoice_id.payment_state', string='Status Pembayaran', readonly=True)
    tanggal_tagihan = fields.Date(related='invoice_id.invoice_date', string='Tanggal Tagihan', readonly=True)
    kode_rumah = fields.Char(related='partner_id.kode_rumah', string='Kode Rumah', readonly=True)

    @api.model
    def create(self, vals):
        """
        Override method create untuk otomatis membuat invoice dan langsung mengkonfirmasi invoice
        saat data disimpan.
        """
        record = super(DashboardData, self).create(vals)

        if record.partner_id and record.layanan_id:
            invoice_date = fields.Date.today()
            due_date = invoice_date + timedelta(days=7)

            invoice = self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': invoice_date,
                'invoice_date_due': due_date,
                'invoice_line_ids': [(0, 0, {
                    'product_id': record.layanan_id.id,
                    'quantity': 1,
                    'price_unit': record.layanan_id.lst_price,
                })]
            })

            record.invoice_id = invoice.id

            invoice.action_post()

        return record

    
    # def _get_data_from_datapenghuni(self, penghuni):
    #     if penghuni:
    #         domain.append(('partner_id.id','in',penghuni))

    # def _get_chart_data(self):
    #     data_penghuni = self._get_data_from_datapenghuni()

    # @api.model
    # def get_dashboard_data(self):
    #     partner_id = self.env.user.partner_id
    #     if not partner_id:
    #         return {}

    #     tagihan_records = self.search([('partner_id', '=', partner_id.id)])

    #     produk_pengeluaran = {}
    #     produk_usage = {}
    #     for tagihan in tagihan_records:
    #         layanan_name = tagihan.layanan_id.name
    #         produk_pengeluaran[layanan_name] = produk_pengeluaran.get(layanan_name, 0) + tagihan.invoice_id.amount_total
    #         produk_usage[layanan_name] = produk_usage.get(layanan_name, 0) + 1

    #     active_tagihan = tagihan_records.filtered(lambda t: t.status_pembayaran == 'not_paid').read(
    #         ['layanan_id', 'tanggal_tagihan', 'status_pembayaran']
    #     )
    #     paid_tagihan = tagihan_records.filtered(lambda t: t.status_pembayaran == 'paid').read(
    #         ['layanan_id', 'tanggal_tagihan', 'status_pembayaran']
    #     )

    #     payment_history = []
    #     for tagihan in tagihan_records:
    #         for line in tagihan.invoice_id.payment_ids:
    #             payment_history.append({
    #                 'tanggal': line.payment_date,
    #                 'jumlah': line.amount,
    #                 'produk': tagihan.layanan_id.name,
    #             })

    #     return {
    #         'produk_pengeluaran': produk_pengeluaran,
    #         'produk_usage': produk_usage,
    #         'active_tagihan': active_tagihan,
    #         'paid_tagihan': paid_tagihan,
    #         'payment_history': payment_history,
    #     }

    def _get_tagihan_data(self, partner_id):
        """Mengambil data tagihan berdasarkan pengguna."""
        return self.search([('partner_id', '=', partner_id.id)])

    def _grouped_tagihan(self, tagihan_records):
        """Mengelompokkan data tagihan berdasarkan layanan."""
        produk_pengeluaran = {}
        produk_usage = {}
        for tagihan in tagihan_records:
            layanan_name = tagihan.layanan_id.name
            produk_pengeluaran[layanan_name] = produk_pengeluaran.get(layanan_name, 0) + tagihan.invoice_id.amount_total
            produk_usage[layanan_name] = produk_usage.get(layanan_name, 0) + 1
        return produk_pengeluaran, produk_usage

    def _get_payment_history(self, tagihan_records):
        """Mendapatkan riwayat pembayaran dari tagihan."""
        payment_history = []
        for tagihan in tagihan_records:
            for line in tagihan.invoice_id.payment_ids:
                payment_history.append({
                    'tanggal': line.payment_date,
                    'jumlah': line.amount,
                    'produk': tagihan.layanan_id.name,
                })
        return payment_history

    def _create_dashboard_data(self, tagihan_records):
        """Menghasilkan data terformat untuk dashboard."""
        active_tagihan = tagihan_records.filtered(lambda t: t.status_pembayaran == 'not_paid').read(
            ['layanan_id', 'tanggal_tagihan', 'status_pembayaran']
        )
        paid_tagihan = tagihan_records.filtered(lambda t: t.status_pembayaran == 'paid').read(
            ['layanan_id', 'tanggal_tagihan', 'status_pembayaran']
        )
        produk_pengeluaran, produk_usage = self._grouped_tagihan(tagihan_records)
        payment_history = self._get_payment_history(tagihan_records)

        return {
            'produk_pengeluaran': produk_pengeluaran,
            'produk_usage': produk_usage,
            'active_tagihan': active_tagihan,
            'paid_tagihan': paid_tagihan,
            'payment_history': payment_history,
        }

    @api.model
    def get_dashboard_data(self):
        """Endpoint untuk mendapatkan data dashboard penghuni."""
        partner_id = self.env.user.partner_id
        if not partner_id:
            return {}

        tagihan_records = self._get_tagihan_data(partner_id)
        return self._create_dashboard_data(tagihan_records)
        
class ResPartner(models.Model):
    _inherit = 'res.partner'

    kode_rumah = fields.Char(string='Kode Rumah', unique=True, required=True)
        # tagihan = fields.Monetary(related='invoice_id.amount_total', string='Jumlah Tagihan', readonly=True)
