from collections import namedtuple
import json
import time
from datetime import datetime

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.addons.procurement.models import procurement
from odoo.exceptions import UserError


class kat_po_hd(models.Model):

    _name = "knitto.po"

    @api.one
    @api.depends("podt_ids")
    def _get_po_order(self):
        self.podt_ids = False
        podt_data = self.env['knitto.po'].search([('name','=',  self.id)])
        if podt_data:
            self.podt_ids = podt_data


    name            = fields.Char("Nomor PO", required=True)
    tanggal         = fields.Date("Tanggal")
    id_supplier     = fields.Char("Id Supplier", required=True)
    tanggal_kirim   = fields.Date("Tanggal Kirim")
    termin          = fields.Char("Termin")
    ppn             = fields.Char("PPN", default="11")
    catatan         = fields.Text("Catatan")
    id_user         = fields.Char("Id User")
    jenis_kain      = fields.Char("Jenis Kain")
    status_hd       = fields.Char("Status")
    so_id           = fields.Many2one('sale.order',string='SO', store=True,)    
    order_ids        = fields.One2many("knitto.po.line", "order_id", "PO Detail")

class kat_po_dt(models.Model):

    _name = "knitto.po.line"

    no_detail       = fields.Char(string='No Detail')
    order_id        = fields.Many2one("knitto.po", ondelete="cascade")
    no_po           = fields.Char(string='No PO')
    id_kain         = fields.Char(string='Id Kain')
    nama_kain       = fields.Char(string='Nama Kain')
    jenis_kain      = fields.Char(string='Jenis Kain')
    kualitas        = fields.Char(string='Kualitas')
    mesin           = fields.Char(string='Mesin')
    gramasi         = fields.Char(string='Gramasi')
    roll            = fields.Char(string='Roll')
    berat           = fields.Char(string='Berat')
    harga           = fields.Char(string='Harga')
    id_warna        = fields.Char(string='Id Warna')
    nama_warna      = fields.Char(string='Nama Warna')
    lebar           = fields.Char(string='Lebar')
    status_dt       = fields.Char(string='Status')
    so_line_id      = fields.Many2one('sale.order.line', string='SO Detail', store=True,)
    # warna_id        = fields.Many2one('makloon.warna', related="so_line_id.color_makloon_id")
