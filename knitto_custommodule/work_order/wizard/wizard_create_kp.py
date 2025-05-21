from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

import time
from datetime import datetime, timedelta

class WizardCreateKp(models.TransientModel):
    _name = 'wizard.create.kp'

    @api.depends('durasi','mesin_date')
    def _compute_waktu_all(self):
        for order in self:
            if order.mesin_date:
                order.mesin_date2 = datetime.strptime(order.mesin_date,"%Y-%m-%d %H:%M:%S") + timedelta(hours=order.durasi)

    so_line_id         = fields.Many2one('sale.order.line', 'WO Line', required=True)
    qty_process        = fields.Integer(string='Qty Process',)
    qty_roll_kp        = fields.Integer(string='Roll KP',)
    qty_kg_kp          = fields.Float(string='Kg KP',)
    qty_mtr_kp         = fields.Float(string='Mtr KP',)
    qty_yds_kp         = fields.Float(string='Yds KP',)
    product_uom        = fields.Many2one('product.uom', 'UOM', required=True)
    product_uom_greige = fields.Many2one('product.uom', 'UOM Greige', required=True)
    type_kp            = fields.Selection(string="Type KP", selection=[
                         ('d','Dyeing'),
                         ('p','Printing'),
                         ], required=True,)
    mesin_id = fields.Many2one('mrp.machine', string='Mesin Plan')
    parent_utama = fields.Integer(string='ID', related="mesin_id.id")
    urutan_partai = fields.Integer(string='Urutan Per Mesin')
    mesin_date = fields.Datetime(string="Date Plan Start",)
    mesin_date2 = fields.Datetime(compute='_compute_waktu_all', string='Date Plan End', store=True)
    durasi = fields.Integer(string='Durasi',default=0)
    parent = fields.Integer(string='Parent', related="mesin_id.id")

    @api.multi
    def createKp(self):
        so_line = self.so_line_id
        if self.qty_process > so_line.qty_remaining :
            raise ValidationError(_("Qty yang akan di proses melebihi qty sisa"))

        kp = self.env['kartu.proses'].create({
            'so_line_id':self.so_line_id.id,
            'so_id':self.so_line_id.order_id.id,
            'lab_id':self.so_line_id.labdip_id.id,
            'qty_process':self.qty_process,
            'qty_roll_kp':self.qty_roll_kp,   
            'qty_kg_kp':self.qty_kg_kp, 
            'qty_mtr_kp':self.qty_mtr_kp,        
            'qty_yds_kp':self.qty_yds_kp,
            'product_uom':self.product_uom.id,       
            'product_uom_greige':self.product_uom_greige.id,
            'type_kp':self.type_kp,
            'mesin_id':self.mesin_id.id,
            'parent_utama':self.parent_utama,
            'urutan_partai':self.urutan_partai,
            'mesin_date':self.mesin_date,
            'mesin_date2':self.mesin_date2,
            'durasi':self.durasi,
            'parent':self.parent
        })

        # return kp
            