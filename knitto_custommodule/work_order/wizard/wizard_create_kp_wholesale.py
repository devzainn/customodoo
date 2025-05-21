from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

import time
import pandas as pd
from datetime import datetime, timedelta


class WizardCreateKPWHolesale(models.TransientModel):
    _name = 'wizard.create.kp.wholesale'

    @api.depends('durasi', 'mesin_date')
    def _compute_waktu_all(self):
        for obj in self:
            if obj.mesin_date:
                obj.mesin_date2 = datetime.strptime(
                    obj.mesin_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=obj.durasi)

    is_active = fields.Boolean(default=True)
    qty_process = fields.Integer(string='Qty Process',)
    qty_roll_kp = fields.Integer(string='Roll KP',)
    qty_kg_kp = fields.Float(string='Kg KP',)
    qty_mtr_kp = fields.Float(string='Mtr KP',)
    qty_yds_kp = fields.Float(string='Yds KP',)
    # product_uom        = fields.Many2one('product.uom', 'UOM', required=True)
    # product_uom_greige = fields.Many2one('product.uom', 'UOM Greige', required=True)
    # type_kp            = fields.Selection(string="Type KP", selection=[
    #                      ('d','Dyeing'),
    #                      ('p','Printing'),
    #                      ], required=True,)
    mesin_id = fields.Many2one('mrp.machine', string='Mesin Plan')
    proses_master_id = fields.Many2one('master.proses', string='Proses')
    parent_utama = fields.Integer(string='ID', related="mesin_id.id")
    urutan_partai = fields.Integer(string='Urutan Per Mesin')
    mesin_date = fields.Datetime(string="Date Plan Start",)
    mesin_date2 = fields.Datetime(
        compute='_compute_waktu_all', string='Date Plan End', store=True)
    date_kp = fields.Date(string="Tanggal", required=True,)
    durasi = fields.Integer(string='Durasi', default=0)
    parent = fields.Integer(string='Parent', related="mesin_id.id")

    line_ids = fields.One2many(
        'wizard.create.kp.wholesale.line', 'wizard_id', string='Lines')
    order = fields.Integer(compute='getOrder', string="Urutan per Mesin")

    is_obat = fields.Boolean(default=True)
    is_greige = fields.Boolean(default=True)
    is_screen = fields.Boolean(default=True)

    @api.onchange('is_active')
    def onchange_is_active(self):
        so_line_ids = self.env.context.get('active_ids', [])
        print '==============onchange_is_active================'
        activeId = self.env.context.get('active_id')
        idSo = self.env['sale.order.line'].browse(activeId).order_id.id
        flowprosesIds = self.env['sale.order'].browse(
            idSo).hanger_code.flowproses_ids.filtered(lambda x: x.proses_master_id.is_kp)
        if len(flowprosesIds) > 1:
            raise UserError(_('Mohon maaf silahkan cek kembali final master proses pada %s, pastikan proses yang berstatus Is Kp hanya ada satu') % (
                self.env['sale.order'].browse(idSo).hanger_code.name))
        self.mesin_id = flowprosesIds.mesin_id.id

        # buat filter proses scouring
        flowprosesmasterIds = self.env['sale.order'].browse(
            idSo).hanger_code.flowproses_ids.filtered(lambda x: x.proses_master_id.kode == 'SC')
        self.proses_master_id = flowprosesmasterIds.proses_master_id.id

        line_ids_value = []

        for so_line in self.env['sale.order.line'].sudo().browse(so_line_ids):

            line_ids_value.append((0, 0, {
                'so_line_id': so_line.id,
                'qty_to_process': so_line.qty_remaining,
            }))

        self.line_ids = line_ids_value


    @api.multi
    def action_create_kp(self):
        self.ensure_one()
        no_urut = self.order
        tanggal_produksi = self.date_kp
        for line in self.line_ids:
            tmpNomorBatch = len(self.env['kartu.proses'].search(
                [('sodet_id', '=', line.so_line_id.id)]).mapped('id'))
            tmpNomorBatch += 1

            tmpOutLast = False
            if(line.so_line_id.batch != False):
                tmpOutLast = line.so_line_id.batch + " - " + str(tmpNomorBatch)
                if line.product_uom_qty == line.qty_to_process:
                    tmpOutLast = line.so_line_id.batch 

            kp = self.env['kartu.proses'].create({
                'sodet_id': line.so_line_id.id,
                'so_id': line.so_id.id,
                # 'lab_id':line.so_line_id.labdip_id.id,
                'lab_id': line.so_line_id.labdip_id.name if(line.so_line_id.id) else False,
                'qty_process': line.qty_to_process,
                'qty_roll_kp': self.qty_roll_kp,
                'qty_kg_kp': self.qty_kg_kp,
                'qty_mtr_kp': self.qty_mtr_kp,
                'qty_yds_kp': self.qty_yds_kp,
                'product_uom': line.so_line_id.uom.id,
                'product_uom_greige': line.so_line_id.uom.id,
                'mesin_id': self.mesin_id.id,
                'parent_utama': self.parent_utama,
                'urutan_partai': no_urut,
                'tanggal_prod': self.date_kp,
                'mesin_date': self.mesin_date,
                'mesin_date2': self.mesin_date2,
                'durasi': self.durasi,
                'parent': self.parent,
                'tanggal': tanggal_produksi,
                # 'product_id':line.so_line_id.product_id.id,
                'product_id': line.so_id.hanger_code.product_id.id,
                'variant_stock': line.so_id.hanger_code.variasi_id.id,
                'greige_code': line.so_id.hanger_code.greige_code,
                'fabric_id': line.so_id.hanger_code.fabric_id,
                'sc_id': line.so_id.sc_id.id,
                'category_sc_id': line.so_id.sc_id.category_id.id,
                'hanger_code': line.so_id.sc_id.td_id.id,
                # 'kp_labdip_resep_ids': listLabdipResep,
                # 'kp_strikeoff_recipe_ids': listStrikeoffResep,
                'proses_ids': [[0, 0, {'name':proses.name,'state': proses.state, 'amount': proses.amount, 
                                'td_id': proses.td_id.id, 'proses_master_id': proses.proses_master_id.id,
                                'lama_proses': proses.lama_proses, 'mesin_id': proses.mesin_id.id, 'no_urut': proses.no_urut, 
                                'f_lebar': proses.f_lebar,'program_id':proses.program_id.id ,'f_lebar_uom': proses.f_lebar_uom.id, 
                                'f_gramasi': proses.f_gramasi, 'f_gramasi_uom': proses.f_gramasi_uom.id, 'f_density': proses.f_density, 
                                'f_susut': proses.f_susut, 'f_susut_uom': proses.f_susut_uom, 'gr_per_mtr': proses.gr_per_mtr, 
                                'mtr_per_kg': proses.mtr_per_kg,'fabric_code':proses.fabric_code ,'fabric_name':proses.fabric_name,
                                'customer_id':proses.customer_id.id,'greige_width':proses.greige_width,'greige_weight':proses.greige_weight,
                                'greige_density':proses.greige_density,'req_width':proses.req_width,'req_weight':proses.req_weight,
                                'f_weight':proses.f_weight,'yard_per_kg':proses.yard_per_kg,'lebar_result':proses.lebar_result,
                                'gramasi_result':proses.gramasi_result,'range_gramasi':proses.range_gramasi,'weight_reduce':proses.weight_reduce,'keterangan':proses.keterangan,
                                'process_type':proses.process_type.id,'density':proses.density,'no_urut_actual':proses.no_urut_actual,
                                'parameter_ids': [[0, 0, {'name':proses.name,'description': param.description, 'state': param.state, 'amount': param.amount, 'td_id': proses.td_id.id, 'parameter_id': param.parameter_id.id,'no_urut': param.no_urut, 'var_proses': param.var_proses, 'nilai': param.nilai, 'uom': param.uom.id}] for param in proses.parameter_ids],
                                'chemical_ids': [[0, 0, {'name':chemical.name,'description': chemical.description, 'state': chemical.state, 'amount': chemical.amount, 'td_id': proses.td_id.id, 'qty': chemical.qty, 'qty_be': chemical.qty_be,'no_urut': chemical.no_urut, 'var_proses': chemical.var_proses, 'product_id': chemical.product_id.id, 'uom_id': chemical.uom_id.id}] for chemical in proses.chemical_ids],
                                'state_parent':proses.state_parent}] for proses in line.so_id.hanger_code.flowproses_ids ],
                'nomor_batch': tmpOutLast,
            })

            if(line.so_id.type == 'dyeing'):
                KitchenLab = self.env['color.kitchen.dyeing'].create({
                    'no_wo'         : line.so_id.id,
                    'sodet_id'      : line.so_line_id.id,
                    'kp_id'         : kp.id,
                    'no_batch'      : tmpOutLast,
                    'tanggal'       : self.date_kp,
                    'mesin_id'      : self.mesin_id.id,
                    'sc_id'         : line.so_id.sc_id.id,
                    'td_id'         : line.so_id.hanger_code.id,
                    'partner_id'    : line.so_id.partner_id.id,
                    'customer_code' : line.so_id.customer_code,
                    'product_id'    : line.so_id.product_id.id,
                    'lebar'         : line.so_id.lebar_finish,
                    'gramasi'       : line.so_id.gramasi_finish,
                    'warna_id'      : line.so_line_id.color_makloon_id.id,
                    'no_warna'      : line.so_line_id.color_no_labdip.id,
                    'labdip_id'     : line.so_line_id.labdip_id.id,
                    'no_map'        : 'STB',
                })

            # START TD
            listColorKitchenDyeing = []
            for out in line.so_id.hanger_code.flowproses_ids:
                if(out.proses_master_id.is_color_kitchen_dyeing == True):
                    for outData in out.chemical_ids:
                        listColorKitchenDyeing.append([0, 0, {
                            'proses_id'     : out.proses_master_id.id,
                            'kode_lab'      : outData.product_id.kode_lab,
                            'product_id'    : outData.product_id.id,
                            'conc'          : outData.qty,
                            'category_resep_test': outData.category_resep_test,
                            'category_uom'  : 'percent' if outData.category_resep_test == 'dye' else 'grl',
                            'sat_id'        : 4 if outData.category_resep_test == 'dye' else 3,
                        }])
                        
                    if(line.so_id.type == 'dyeing'):
                        KitchenTD = self.env['color.kitchen.dyeing'].create({
                            'no_wo'             : line.so_id.id,
                            'sodet_id'          : line.so_line_id.id,
                            'td_proses_id'      : out.id,
                            'kp_id'             : kp.id,
                            'no_batch'          : tmpOutLast,
                            'tanggal'           : self.date_kp,
                            'mesin_id'          : self.mesin_id.id,
                            'sc_id'             : line.so_id.sc_id.id,
                            'td_id'             : line.so_id.hanger_code.id,
                            'partner_id'        : line.so_id.partner_id.id,
                            'customer_code'     : line.so_id.customer_code,
                            'product_id'        : line.so_id.product_id.id,
                            'lebar'             : line.so_id.lebar_finish,
                            'gramasi'           : line.so_id.gramasi_finish,
                            'warna_id'          : line.so_line_id.color_makloon_id.id,
                            'no_map'            : out.proses_master_id.name,
                        })
                        KitchenTD.action_load_receipt_lab()
                        
                    if(line.so_id.type == 'printing'):
                        KitchenTD = self.env['color.kitchen.dyeing'].create({
                            'tanggal'           : self.date_kp,
                            'mesin_id'          : self.mesin_id.id,
                            'no_wo'             : line.so_id.id,
                            'sodet_id'          : line.so_line_id.id,
                            'warna_id'          : line.so_line_id.color_makloon_id.id,
                            'td_proses_id'      : out.id,
                            'kp_id'             : kp.id,
                            'no_batch'          : tmpOutLast,
                            'no_map'            : out.proses_master_id.name,
                        })
                        KitchenTD.action_load_receipt_lab()
            # END TD


            no_urut += 1
        message_id = self.env['wizard.message'].create(
            {'message': _("Kartu Proses sukses dibuat")})
        return {
            'name': _('Sukses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.message',
            # pass the id
            'res_id': message_id.id,
            'target': 'new'
        }

    @api.depends('mesin_id', 'date_kp')
    def getOrder(self):
        if self.mesin_id and self.date_kp:
            rec = self.env['kartu.proses'].search(
                [('mesin_id', '=', self.mesin_id.id), ('tanggal_prod', '=', self.date_kp)])
            max_no_urut = 0
            if rec:
                max_no_urut = max(rec.mapped('urutan_partai'))
            self.order = max_no_urut + 1
        else:
            self.order = 1


class WizardCreateKPWHolesaleLine(models.TransientModel):
    _name = 'wizard.create.kp.wholesale.line'

    wizard_id = fields.Many2one(
        'wizard.create.kp.wholesale', string="General Data")
    so_line_id = fields.Many2one('sale.order.line', string="WO Line")
    so_id = fields.Many2one(related='so_line_id.order_id', string='No WO')
    contract_id = fields.Many2one(
        related='so_line_id.contract_id', string='No SC')
    color = fields.Many2one(related='so_line_id.color', string='Color')
    product_uom_qty = fields.Float(
        related='so_line_id.product_uom_qty', string="Qty Order")
    qty_remaining = fields.Float(
        related='so_line_id.qty_remaining', string="Qty Sisa")
    qty_to_process = fields.Float(string="Qty Untuk Di proses")

    @api.onchange('qty_to_process')
    def onchangeQtytoProcess(self):
        if self.qty_to_process > self.qty_remaining:
            self.qty_to_process = self.qty_remaining
        if self.qty_to_process < 0:
            self.qty_to_process = 0
