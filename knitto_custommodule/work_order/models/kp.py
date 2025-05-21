from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ColorKitchenDyeing(models.Model):
    _inherit = 'color.kitchen.dyeing'


    batch_ref = fields.Char(string='Batch Ref', related='kp_id.batch_ref')
    wo_ref = fields.Char(string='WO Ref', related='kp_id.wo_ref')

    @api.onchange('kp_id')
    def onchange_kp_id(self):
        for rec in self:
            rec.warna_id        = rec.kp_id.cw.id,
            rec.no_warna        = rec.kp_id.nomor_warna.id,
            rec.labdip_id       = rec.kp_id.nomor_warna.labdip_id.id,
            rec.no_batch        = rec.kp_id.nomor_batch,

class KPMadun(models.Model):
    _inherit = 'kartu.proses'

    # product_mkt_id      = fields.Many2one('product.product',string='PRODUCT NAME', related='so_id.product_id',)
    delivery_date       = fields.Date(string='DELIVERY DATE', related='so_id.delivery_date', store=True,)
    kode_customer       = fields.Char(string='KODE CUSTOMER', related='partner_id.ref', store=True,)
    # code_customer       = fields.Char(string='Code Customer', compute='get_kode_customer',) #buat group by dan search kp
    jum_order           = fields.Float(string='JUMLAH ORDER', related='so_id.total_product_uom_qty',)
    susut               = fields.Float(string='SUSUT', related='td_no.shrinkage',)
    colorway            = fields.Integer(String='COLORWAY', related='strike_off_id.jum_colorway')

    motif_id            = fields.Char(string='MOTIF', related='so_id.design_id.motive', store=True,)
    design_code         = fields.Char(string='NO. DESIGN', related='so_id.design_id.design_code', store=True,)
    nomor_batch         = fields.Char(string='NO. BATCH')
    cw                  = fields.Many2one('makloon.warna', string='CW', related='sodet_id.color_makloon_id')
    wo_ref              = fields.Char(String='WO Ref', related='so_id.origin', readonly=True)
    nomor_warna         = fields.Many2one('labdip.warna', string='NO. WARNA', related='sodet_id.color_no_labdip')
    strike_off_id       = fields.Many2one('strikeoff', string='STRIKE OFF', related='so_id.strike_off_id')
    jum_screen          = fields.Integer(string='JUMLAH SCREEN', related='strike_off_id.jum_screen')
    dasar_kain          = fields.Many2one('master.fabric.base',string='DASAR KAIN', related='strike_off_id.fabric_base_id')
    proses              = fields.Char(string='PROSES')

    mesin_name          = fields.Char(string='MESIN', related='mesin_id.name', store=True,)
    cw_name             = fields.Char(string='CW', related='cw.name', store=True,)
    nomor_warna_name    = fields.Char(string='NO. WARNA', related='nomor_warna.name', store=True,)
    process_id_name     = fields.Char(string='Process', related='process_id.name', store=True,)
    so_note             = fields.Text(string='SO Note', related='so_id.note', store=True,)

    greige_name         = fields.Many2one('product.product', string='GREIGE NAME', related='td_no.product_id')
    kode_greige         = fields.Char(string='KODE GREY', related='td_no.greige_code')
    td_no               = fields.Many2one('test.development', string='TD NO', related='so_id.hanger_code')
    fabric_type         = fields.Many2one('tj.stock.variasi.kategori',String="FABRIC TYPE", related="td_no.variasi_id.kategori_id")
    lebar_kain_finish   = fields.Char(string='LEBAR FINISH', related='td_no.lebar_greige_target', store=True,)
    gramasi_kain_finish = fields.Char(string='GRAMASI FINISH', related='td_no.gramasi_greige_target', store=True,)
    range_gramasi_kain  = fields.Char(string='RANGE GRAMASI FINISH', related='td_no.range_gramasi_target')
    density_finish      = fields.Char(string='DENSITY FINISH', related='td_no.density_target')
    
    kategori            = fields.Many2one('type.ship', string='KATEGORI', related='sc_id.type_ship_id')
    grading             = fields.Selection(string='GRADING', related='sc_id.grading')
    piece_length        = fields.Integer(string='PIECE LENGTH', related='sc_id.piece_length')
    max_join_pcs        = fields.Char(string='MAX JOIN PCS', related='sc_id.max_joint_pieces')
    packing             = fields.Many2one('sale.contract.packing',string='PACKING',related='sc_id.packing')
    acessories          = fields.Many2one('accessories',string='ACESSORIES',related='sc_id.accessories_id')
    hang_tag            = fields.Many2one('hang.tag',string='HANG TAG',related='sc_id.hang_tag_id')
    fabric_code         = fields.Char(string='Fabric Code', related='so_id.hanger_code.fabric_id')
    wo_date             = fields.Date(string='WO Date', related='so_id.wo_date')
    type_wo = fields.Selection(
        selection=[
            ('dyeing', 'Work Order Dyeing'),
            ('printing', 'Work Order Printing'),
            ],
        string='Type', compute="_compute_type_wo")
    batch_ref = fields.Char(string="Batch Ref")
    variasi_id = fields.Many2one('tj.stock.variasi', string='Variasi', related="so_id.hanger_code.variasi_id")
    status_terkini = fields.Selection([("inspected","Inspected"),("receive_gd_jadi","Receive Gd Jadi"), ("expedisi","expedisi"), ("terkirim","terkirim")], string='Status Terkini')
    lot_jadi_ids = fields.One2many('stock.production.lot', 'kp_id', string='Lot Jadi')
    qty_delivery = fields.Float(compute='_compute_qty_delivery', string='Qty Delivery')
    x_qty_delivery = fields.Float(string='Qty Delivery', related='qty_delivery', store=True,)
    
    @api.depends('status_terkini', 'lot_jadi_ids')
    def _compute_qty_delivery(self):
        for rec in self:
            qty_delivery = sum(rec.lot_jadi_ids.mapped('product_sold'))
            rec.qty_delivery = qty_delivery
    
    

    @api.depends('so_id')
    def _compute_type_wo(self):
        for rec in self:
            rec.type_wo = rec.so_id.type
