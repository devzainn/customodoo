from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero, float_compare
from datetime import datetime, timedelta
import time
import logging

_logger = logging.getLogger(__name__)

opsi_permartaian = [
    ('not_worked','Belum Dikerjakan'),
    ('in_progress','Sedang Dikerjakan'),
    ('done','Selesai'),
]


opsi_pengiriman = [
    ('not_delivered','Belum Dikirim'),
    ('partial','Sudah dikirim sebagian'),
    ('done','Selesai'),
]

class WorkOrder(models.Model):
    _inherit = 'sale.order'

    def _default_delivery_date(self):
        return fields.Date.context_today(self)

    wo_date = fields.Date('WO Date', default=_default_delivery_date)
    customer_code = fields.Char('Customer Code',related="partner_id.ref",store=True)
    po_id = fields.Many2one('purchase.order', 'PO No') #many2one?
    category_id = fields.Char("Category") #many2one?
    # delivery_date = fields.Date('Delivery Date',store=True, required=True)
    delivery_date = fields.Date(string='Delivery Date',)
    wo_no = fields.Char('Work Order No')
    prod_type = fields.Many2one('sale.contract.category', string='Category',related="sc_id.category_id",store=True)
    m_j = fields.Char('M/J')
    w_k = fields.Char('W/K')
    batch_no = fields.Char('BATCH NO.') #update dari KP
    # hanger_code = fields.Char('Hanger Code')
    hanger_code = fields.Many2one('test.development', String='Hanger Code',store=True,
    #  domain= lambda self:[('id','in',self.domain_hanger_code())]
     )
    # hanger_code = fields.Many2one('test.development', String='Hanger Code')

    hanger_greige = fields.Many2one('product.product')
    hanger_variasi = fields.Many2one('tj.stock.variasi')
    strike_off_id = fields.Many2one('strikeoff', string='Strike Off')
    greige_name = fields.Char(string='Greige Name',related="sc_id.greige_name",store=True)
    product_id  = fields.Many2one(string='Product', related="sc_id.product_id",store=True)
    # greige_name = fields.Many2one(comodel_name="product.product", String='Greige Name')
    # construction = fields.Char('Construction')
    construction = fields.Many2one('kontruksi', String='Construction',related="sc_id.td_id.construction",store=True)
    # design_no = fields.Char('Design No')
    master_design_no = fields.Many2one('makloon.design', String='Design No',related="strike_off_id.design_id",store=True)
    # master_design_no = fields.Many2one('master.design', String='Design No',related="strike_off_id.design_id",store=True)
    article_name = fields.Char('Article Name',related="strike_off_id.motif",store=True)
     # related="design_no.motif"
    # fabric_code = fields.Many2one(comodel_name="product.product", String='Fabric Code') #many2one?
    # fabric_code    = fields.Char(string='Fabric Code',related='sc_id.td_id.fabric_id',store=True)
    fabric_code    = fields.Char(string='Fabric Code')
    sj_greige = fields.Many2one('stock.picking', String='SJ Greige') #many2one?
    request_width = fields.Char('Req. Width')
    request_weight = fields.Char('Req. Weight')
    percentage_shrinkage = fields.Char('% Shrinkage', related='contract_id.persen_shrinkage',store=True)
    density = fields.Char('Density',related="contract_id.td_id.fabric_density",store=True)
    fabric_base = fields.Char('Fabric Base') #many2one?
    wo_note = fields.Char('Note')
    labdip_id = fields.Many2one('labdip', String='Labdip No')

    sales_type    = fields.Selection(selection=[('makloon','Makloon'),('jual','Jual')], string='Sale Type',)
    process_id    = fields.Many2one('sale.contract.process', string='Process',)
    toleransi_grade_b           = fields.Float(string='Toleransi Grade B',)
    toleransi_susut             = fields.Float(string='Toleransi Susut', related="sc_id.toleransi_susut")
    lebar_finish                = fields.Char(string='Lebar Finish')
    # lebar_finish_uom            = fields.Many2one('product.uom', string='Lebar Uom', domain=[('id', 'in', [106,77,3])])
    gramasi_finish              = fields.Char(string='Gramasi Finish',)
    # gramasi_finish_uom          = fields.Many2one('product.uom', string='Gramasi Uom', domain=[('id', 'in', [106,77,3])])
    potongan_pinggir            = fields.Selection(selection=[('yes', 'Yes'),('no', 'No'),],string='Potongan Pinggir',)

    grading                     = fields.Selection([(10,'10 Points'),(4,'4 Points')],'Grading',default=10,)
    max_joint_pieces            = fields.Char('Max Join Pieces',)
    piece_length                = fields.Integer('Piece Length', )
    packing                     = fields.Many2one('sale.contract.packing',string='Packing',)
    accessories_id              = fields.Many2one('accessories',string='Accessories',)
    hang_tag_id                 = fields.Many2one('hang.tag',string='Hang Tag',)
    customer_payment_term       = fields.Many2one('account.payment.term',string='TOP', related="sc_id.customer_payment_term")
    type = fields.Selection(
        selection=[
            ('dyeing', 'Work Order Dyeing'),
            ('printing', 'Work Order Printing'),
            ],
        string='Type', default='dyeing', change_default=True,)


    color_id = fields.Many2one('labdip.warna', string='Color')
    color_code = fields.Char(string='Color Code')
    qty_pesanan = fields.Float(string='Qty', compute='get_qty_pesanan')
    uom_pesanan_id = fields.Many2one('product.uom', string='Uom')
    note = fields.Text(string='Note')
    status_so = fields.Char(string='Status SO')
    design_id = fields.Many2one('makloon.design', string="Design")
    sc_id = fields.Many2one('sale.contract', string='Sale Contract')
    state = fields.Selection(selection_add=[("draft_wo", "Draft"),("confirm_wo","Confirm")])
    note = fields.Text(string='Note')
    piece_length_uom      = fields.Many2one('product.uom',string='Piece Length Uom', default=3, domain="[('id', 'in', [106,77,3])]")
    type_sc_category = fields.Selection(selection=[('dyeing', 'Work Order Dyeing'),('printing', 'Work Order Printing'),],string='Type',related="type")

    type_wo = fields.Selection([("stock","Re Stock"),("order","Fresh Order")], string='Type Wo', )
    qty_minimum                = fields.Float(string='Qty Minimum', related="sc_id.min_qty_color")
    is_work_order = fields.Boolean(string='Is Work Order')


    is_available_stock = fields.Boolean(default=True)
    is_after_check = fields.Boolean(default=False)
    is_notulen = fields.Boolean(string='Is Notulen', default=False)
    notulen    = fields.Char(string='Notulen',)

    is_mlot       = fields.Boolean(string='Is Mlot', related='hanger_code.is_mlot')
    states_greige = fields.Selection([("ada","Ada"),("approve","Approve")], string='Status Order', readonly=True, compute="_compute_states_greige_")
    # states_greige_store = fields.Char(related='states_greige', string='Status Order', store=True)
    order_pertama    = fields.Char(string='Order Pertama', compute="_compute_order_pertama")
    # can_create_notulen = fields.Boolean(compute='_compute_can_create_notulen')


    # inventory_id = fields.Many2one('stock.inventory', string='Inventory Adjustment')
    rak_variasi_summary_ids = fields.One2many('sale.order.rak.variasi','order_id')
    uom_id = fields.Many2one('product.uom', string='Uom')
    total_product_uom_qty = fields.Float(compute='_compute_total', string='Total', store=False)
    total_qty_product_greige = fields.Float(string='Quantity Greige', compute="_compute_total_qty_product_greige"
    #  related='hanger_code.product_id.qty_available'
     )
    product_greige_id = fields.Many2one('product.product', string='Product Greige', related="hanger_code.product_id")
    product_variasi_id = fields.Many2one('tj.stock.variasi', string='Variasi', related="hanger_code.variasi_id")    
    approved_rnd = fields.Boolean(string='Approved Rnd',default=False)
    qty_available = fields.Float(string='Qty Available', compute="_compute_qty_available")
    qty_reserve = fields.Float(string='Qty Reserve', compute="_compute_qty_available")
    is_selesai = fields.Boolean(string='Is Selesai', default=False)
    greige_code = fields.Char(string='Greige Code', related="hanger_code.greige_code")
    check_states = fields.Selection([("no_mlot","No Mlot"),("isi_notulen","isi Notulen"),("approve_rnd","Approve Rnd"),
                                    ("approve_rnd","Approve Rnd"),("approve","Approve"),("ada","Ada"),
                                    ("approve","Approve"),("ada_mlot","Ada Mlot"),("mlot_draft","Mlot Draft"),("mlot_approve","Mlot Approve"),("done","done")], string='Status Order', readonly=True, copy=False)
    
    is_hanger_change = fields.Boolean(string='Hanger was Changed',default=False)

    @api.depends('order_line.product_uom_qty')
    def get_qty_pesanan(self):
        for rec in self:
            qty = rec.order_line.mapped('product_uom_qty')
            rec.qty_pesanan = sum(qty)
    

    
    @api.depends('contract_id')
    @api.onchange('hanger_code')
    def onchange_hanger_code(self):
        kp_ids = self.env['kartu.proses'].sudo().search([('so_id','=',self._origin.id)]).filtered(lambda x:x.state == 'draft')
        if kp_ids:
            self.update({"is_hanger_change":True})
        _logger.warning('='*40)
        _logger.warning('ON CHANGE')
        _logger.warning(self.is_hanger_change)
        _logger.warning('='*40)
    
    
    
    @api.one
    def _compute_qty_available(self):
        print '==========qty available==========='
        print self.picking_ids.ids
        stockPackOperationObj = self.env['stock.pack.operation'].search([
            ('picking_id.picking_type_id','=',178),
            ('product_id','=',self.product_greige_id.id),
            ('variasi_id','=',self.product_variasi_id.id),
            ('picking_id.state','not in',['cancel','done'])
            ])
        for rec in self:
            # rec.qty_available = sum(stockPackOperationObj.mapped('product_qty'))
            # rec.qty_reserve = rec.total_qty_product_greige - sum(stockPackOperationObj.mapped('available_qty'))
            # woObj = self.env['sale.order'].search([('is_work_order','=',True),('picking_ids.state','!=',)])
            # rec.qty_reserve = rec.total_qty_product_greige - sum(stockPackOperationObj.mapped('available_qty'))
            rec.qty_reserve = sum(stockPackOperationObj.mapped('product_qty'))
            rec.qty_available = rec.total_qty_product_greige - sum(stockPackOperationObj.mapped('product_qty'))




    @api.multi
    def unlink(self):
        for order in self:
            if order.state not in ('draft', 'cancel', 'draft_wo'):
                raise UserError(_('You can not delete a sent quotation or a sales order! Try to cancel it before.'))
            query = """ DELETE FROM sale_order where id = %s;
                        DELETE FROM sale_order_line where order_id = %s;""" % (str(order.id),str(order.id))
            self._cr.execute(query)

    @api.multi
    def action_approve_rnd(self):
        self.approved_rnd = True  
        self.check_states = self.states_greige

    
    def check_td(self):
        if self.hanger_code.mlot_id:
            # self.check_states = 'ada_mlot'
            if self.hanger_code.mlot_id.state == 'draft':
                self.check_states = 'isi_notulen'
            elif self.hanger_code.mlot_id.state == 'approve_rnd':
                if self.hanger_code.mlot_id.state == 'approve_rnd':
                # if self.hanger_code.is_order_pertama == True and self.hanger_code.mlot_id.state == 'approve_rnd':
                    self.check_states = ''
                    action = self.env.ref('work_order.pop_up_warning_action').read()[0]
                    return action
            elif self.hanger_code.mlot_id.state == 'approve':
                self.hanger_code = self.hanger_code.mlot_id.id
                self.check_states = self.states_greige
        elif self.hanger_code.is_mlot == True:
            self.check_states = self.states_greige


    @api.depends('is_notulen')
    def _compute_order_pertama(self):
        for rec in self:
            if rec.is_notulen:
                rec.order_pertama='Order Pertama'

    @api.one
    def _compute_total_qty_product_greige(self):
        # quantObj = self.env['stock.quant'].search([('product_id','=',self.product_greige_id.id),('reservation_id','=',False),('location_id','=',34),('lot_id.variasi_id','=',self.product_variasi_id.id)])
        variasiIds = []
        tdObj = self.env['test.development'].search([('product_mkt_id','=',self.product_id.id),('process_sc','=',self.process_id.id)])
        for td in tdObj:
            if td.variasi_id.id:
                variasiIds.append(td.variasi_id.id)
        print '====compute_total'
        print variasiIds
        print self.env.user.company_id.id
        stockProductionLot = self.env['stock.production.lot'].search([
                                                                    #   ('product_id','=',self.product_id.id),
                                                                      ('warehouse_id','=',2),
                                                                      ('variasi_id','in',list(dict.fromkeys(variasiIds))),
                                                                      ('state','=','available'),
                                                                      ('product_saldo','>',0)
                                                                      ])
        for rec in self:
            rec.total_qty_product_greige = sum(stockProductionLot.mapped('product_saldo'))

    @api.depends('order_line')
    def _compute_total(self):
        for order_doc in self:
            order_doc.total_product_uom_qty = sum(order_doc.order_line.mapped('product_uom_qty'))

    
    @api.depends('total_product_uom_qty','total_qty_product_greige')
    def _compute_states_greige_(self):
        for rec in self:
            if rec.total_product_uom_qty > rec.total_qty_product_greige:
                rec.states_greige = 'approve'
            elif rec.total_product_uom_qty < rec.total_qty_product_greige:
                rec.states_greige = 'ada'
            elif rec.total_product_uom_qty == rec.total_qty_product_greige:
                rec.states_greige = 'ada'
    
    # @api.multi
    # def _compute_states_greige_(self):
    #     for rec in self:
    #         if rec.total_product_uom_qty > rec.total_qty_product_greige:
    #             rec.states_greige = 'approve'
    #             update({'states_greige':rec.states_greige})
    #         elif rec.total_product_uom_qty < rec.total_qty_product_greige:
    #             rec.states_greige = 'ada'
    #             update({'states_greige':rec.states_greige})



    # @api.depends('td_id')
    # def _compute_can_create_notulen(self):
    #     for rec in self:
    #         rec.can_create_notulen = 

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         rec.lebar_finish_uom = rec.product_id.uom_id.id
    #         rec.gramasi_finish_uom = rec.product_id.uom_id.id


    @api.multi
    def rak_variasi_wizard(self):
        
        return {
                'type': 'ir.actions.act_window',
                'name': 'Information Stock Greige',
                'res_model': 'sale.order.rak.variasi.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('work_order.sale_order_rak_variasi_wizard_form_2',False).id,
                'target': 'new',
                #'context':{'product_id':self.product_id.id}
                'context':{'hanger_code':self.hanger_code.id}
        }



    @api.multi
    def open_wizard_notulen(self):
        if self.hanger_code.mlot_id:
            if self.hanger_code.is_order_pertama == True and self.hanger_code.mlot_id.state == 'approve_rnd':
                raise UserError('Silahkan Klik Button Check terlebih dahulu.')
        ref = self.env.ref('work_order.notulen_wizard_wo_action')
        return ref.read()[0]

    def buka_wizard_exact_tree_form(self):
        action = self.env.ref('account.view_account_supplier_payment_tree')
        result = action.read()[0]
        imd = self.env['ir.model.data']
        list_view_id = imd.xmlid_to_res_id('account.view_account_supplier_payment_tree')
        form_view_id = imd.xmlid_to_res_id('account.view_account_payment_form')
        result['domain'] = "[('id', 'in', " + str(self.advance_ids.ids) + ")]"
        return {
            'name': 'Advances',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
            'domain' : result.get('domain'),
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
        }
    

    # Original Pak Yuniar

    # @api.multi
    # def action_check_stock(self):
        
    #     res = super(WorkOrder, self).action_confirm()

    #     if self.is_mlot == False and self.notulen == False:
    #         raise UserError('Silahkan Klik tombol Notulen terlebih dahulu.')
    #     self.states_greige = 'ada'
    #     #print " RES ::::::: ", res
    #     self.is_after_check = True
    #     stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',self.id)])

    #     #print "STOCK PICKING CHECK ", stockPickingCheck
    #     for rec in stockPickingCheck:
            
    #         not_available_stock = ''
    #         product_loc_lot_qty = {}
    #         if rec.state != 'assigned' :
    #             for line in rec.move_lines :
    #                 if line.location_id.usage == 'internal' :
    #                     location_ids = self.env['stock.location'].search([('id','child_of',line.location_id.id)])
    #                     product_loc_lot_qty[(line.product_id, location_ids, line.restrict_lot_id)] = product_loc_lot_qty.get((line.product_id, location_ids, line.restrict_lot_id), 0) + line.product_uom_qty
    #         else :
    #             for line in rec.pack_operation_product_ids :
    #                 if line.location_id.usage == 'internal' :
    #                     if not line.pack_lot_ids :
    #                         product_loc_lot_qty[(line.product_id, line.location_id, False)] = product_loc_lot_qty.get((line.product_id, line.location_id, False), 0) + line.qty_done
    #                     else :
    #                         for pl in line.pack_lot_ids :
    #                             product_loc_lot_qty[(line.product_id, line.location_id, pl.lot_id)] = product_loc_lot_qty.get((line.product_id, line.location_id, pl.lot_id), 0) + pl.qty
            
    #         for prod_loc_lot, qty in product_loc_lot_qty.items():
    #             prod, loc_ids, lot = prod_loc_lot
    #             loc_tuple_ids = str(tuple(loc_ids.ids)).replace(',)',')')
    #             if not lot :
    #                 query = """
    #                     SELECT
    #                         SUM(q.qty) as qty
    #                     FROM
    #                         stock_quant q
    #                     WHERE
    #                         location_id in %s
    #                         AND product_id = %s
    #                 """%(loc_tuple_ids, prod.id)
    #                 self._cr.execute(query)
    #                 result = self._cr.dictfetchall()
    #                 available_qty = result[0]['qty'] or 0
                    
    #                 if available_qty < qty :
    #                     not_available_stock += '\n product %s di lokasi %s: diperlukan (%s) tersedia (%s)'%(prod.name_get()[0][1], ', '.join(loc.name_get()[0][1] for loc in loc_ids), '{:,.2f}'.format(qty), '{:,.2f}'.format(available_qty))
    #             else :
    #                 query = """
    #                     SELECT
    #                         SUM(q.qty) as qty
    #                     FROM
    #                         stock_quant q
    #                     WHERE
    #                         location_id in %s
    #                         AND product_id = %s
    #                         AND lot_id = %s
    #                 """%(loc_tuple_ids, prod.id, lot.id)
    #                 self._cr.execute(query)
    #                 result = self._cr.dictfetchall()
    #                 available_qty = result[0]['qty'] or 0
                    
    #                 if available_qty < qty :
    #                     not_available_stock += '\n product %s lot %s di lokasi %s: diperlukan (%s) tersedia (%s)'%(prod.name_get()[0][1], lot.name, ', '.join(loc.name_get()[0][1] for loc in loc_ids), '{:,.2f}'.format(qty), '{:,.2f}'.format(available_qty))
                    

    #                 # Opname code validation
    #                 if rec.picking_type_id.warehouse_id.code == 'GDJ':
    #                     query = """
    #                         SELECT
    #                             a.name as opname_code, d.name as lot
    #                         FROM
    #                             stock_opname_code a
    #                             LEFT JOIN
    #                             stock_opname_code_lot b ON b.opname_code_id = a.id
    #                             LEFT JOIN
    #                             stock_opname_code_lot_stock_production_lot_rel c ON b.id = c.stock_opname_code_lot_id
    #                             LEFT JOIN
    #                             stock_production_lot d ON c.stock_production_lot_id = d.id
    #                         WHERE
    #                             a.location_id in %s AND
    #                             a.state in ('draft','calculate') AND
    #                             d.product_id = %s AND
    #                             c.stock_production_lot_id = %s
    #                     """%(loc_tuple_ids, prod.id, lot.id)
    #                     self._cr.execute(query)
    #                     result = self._cr.dictfetchall()

    #                     if result:
                            
    #                         rec.action_cancel()
    #                         rec.action_draft_picking()
    #                         self.is_available_stock = False
    #                         self.state = 'draft_wo'
                            

    #         if not_available_stock :
                
    #             rec.action_cancel()
    #             rec.action_draft_picking()
    #             self.is_available_stock = False
    #             self.state = 'draft_wo'        

    #     #raise ValidationError(_("BLADUS !"))


    @api.multi
    def action_check_stock(self):
        
        # res = super(WorkOrder, self).action_confirm()

        # if self.is_mlot == False and self.notulen == False:
        #     raise UserError('Silahkan Klik tombol Notulen terlebih dahulu.')
        #print " RES ::::::: ", res
        self.is_after_check = True
        stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',self.id)])

        #print "STOCK PICKING CHECK ", stockPickingCheck
        for rec in stockPickingCheck:
            
            not_available_stock = ''
            product_loc_lot_qty = {}
            if rec.state != 'assigned' :
                for line in rec.move_lines :
                    if line.location_id.usage == 'internal' :
                        location_ids = self.env['stock.location'].search([('id','child_of',line.location_id.id)])
                        product_loc_lot_qty[(line.product_id, location_ids, line.restrict_lot_id)] = product_loc_lot_qty.get((line.product_id, location_ids, line.restrict_lot_id), 0) + line.product_uom_qty
            else :
                for line in rec.pack_operation_product_ids :
                    if line.location_id.usage == 'internal' :
                        if not line.pack_lot_ids :
                            product_loc_lot_qty[(line.product_id, line.location_id, False)] = product_loc_lot_qty.get((line.product_id, line.location_id, False), 0) + line.qty_done
                        else :
                            for pl in line.pack_lot_ids :
                                product_loc_lot_qty[(line.product_id, line.location_id, pl.lot_id)] = product_loc_lot_qty.get((line.product_id, line.location_id, pl.lot_id), 0) + pl.qty
            
            for prod_loc_lot, qty in product_loc_lot_qty.items():
                prod, loc_ids, lot = prod_loc_lot
                loc_tuple_ids = str(tuple(loc_ids.ids)).replace(',)',')')
                if not lot :
                    query = """
                        SELECT
                            SUM(q.qty) as qty
                        FROM
                            stock_quant q
                        WHERE
                            location_id in %s
                            AND product_id = %s
                    """%(loc_tuple_ids, prod.id)
                    self._cr.execute(query)
                    result = self._cr.dictfetchall()
                    available_qty = result[0]['qty'] or 0
                    
                    if available_qty < qty :
                        not_available_stock += '\n product %s di lokasi %s: diperlukan (%s) tersedia (%s)'%(prod.name_get()[0][1], ', '.join(loc.name_get()[0][1] for loc in loc_ids), '{:,.2f}'.format(qty), '{:,.2f}'.format(available_qty))
                else :
                    query = """
                        SELECT
                            SUM(q.qty) as qty
                        FROM
                            stock_quant q
                        WHERE
                            location_id in %s
                            AND product_id = %s
                            AND lot_id = %s
                    """%(loc_tuple_ids, prod.id, lot.id)
                    self._cr.execute(query)
                    result = self._cr.dictfetchall()
                    available_qty = result[0]['qty'] or 0
                    
                    if available_qty < qty :
                        not_available_stock += '\n product %s lot %s di lokasi %s: diperlukan (%s) tersedia (%s)'%(prod.name_get()[0][1], lot.name, ', '.join(loc.name_get()[0][1] for loc in loc_ids), '{:,.2f}'.format(qty), '{:,.2f}'.format(available_qty))
                    

                    # Opname code validation
                    if rec.picking_type_id.warehouse_id.code == 'GDJ':
                        query = """
                            SELECT
                                a.name as opname_code, d.name as lot
                            FROM
                                stock_opname_code a
                                LEFT JOIN
                                stock_opname_code_lot b ON b.opname_code_id = a.id
                                LEFT JOIN
                                stock_opname_code_lot_stock_production_lot_rel c ON b.id = c.stock_opname_code_lot_id
                                LEFT JOIN
                                stock_production_lot d ON c.stock_production_lot_id = d.id
                            WHERE
                                a.location_id in %s AND
                                a.state in ('draft','calculate') AND
                                d.product_id = %s AND
                                c.stock_production_lot_id = %s
                        """%(loc_tuple_ids, prod.id, lot.id)
                        self._cr.execute(query)
                        result = self._cr.dictfetchall()

                        if result:
                            
                            rec.action_cancel()
                            rec.action_draft_picking()
                            self.is_available_stock = False
                            self.state = 'draft_wo'
                            

            if not_available_stock :
                
                rec.action_cancel()
                rec.action_draft_picking()
                self.is_available_stock = False
                self.state = 'draft_wo'        



    @api.multi
    def action_confirm_wo(self):
        for rec in self:
            if(rec.state=='confirm_wo'):
                raise ValidationError(_("Work / Sale order dengan nomor : "+ rec.name + " sudah berstatus confirm. Anda tidak bisa melakukan konfirmasi ulang"))
            rec.action_confirm()
            seq_id = self.env['ir.sequence']
            context = self.env.context
            # if context.get('is_work_order'):
            code = ''
            if self.is_work_order == True:
                if rec.type == 'dyeing' :
                    rec.name = seq_id.next_by_code('wo.dyeing')
                    code = 'D'
                elif rec.type == 'printing':
                    rec.name = seq_id.next_by_code('wo.printing')
                    code = 'P'
                rec.create_planning_global()
                if rec.is_mlot == False:
                    rec.hanger_code.write({'is_order_pertama':True})
                for wo_id in self :
                    no = 1
                    for line in wo_id.order_line:
                        # line.batch = wo_id.name.split('/')[3] +  "-" +self.env['ir.sequence'].next_by_code('no.batch')
                        monthDict = {"01" : "A",
                                    "02" : "B",
                                    "03" : "C",
                                    "04" : "D",
                                    "05" : "E",
                                    "06" : "F",
                                    "07" : "G",
                                    "08" : "H",
                                    "09" : "I",
                                    "10" : "J",
                                    "11" : "K",
                                    "12" : "L"}
                        bulanCreateKp = monthDict.get(datetime.now().strftime("%m"))
                        bulanWo  = wo_id.name.split('/')[2]
                        noUrutWo = wo_id.name.split('/')[3]
                        line.batch = code + bulanCreateKp + str(no) + '-' +bulanWo + noUrutWo
                        no += 1

            # ------- END action_assign_manager 


            stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',rec.id)])
            for res in stockPickingCheck:
                #print " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> "
                originWo = ' (' +  rec.origin + ')' if rec.origin else ''
                res.origin = rec.name + originWo
                res.picking_type_id = 178
                res.location_dest_id = self.env['stock.picking.type'].browse(178).default_location_dest_id.id
                
                if(res.move_lines and rec.hanger_code.id):
                    if(rec.hanger_code.variasi_id.id):
                        for outMove in res.move_lines:
                            outMove.variasi_id = rec.hanger_code.variasi_id.id
                            outMove.product_uom_qty = outMove.product_uom_qty + ((outMove.product_uom_qty * rec.hanger_code.shrinkage) / 100)

                if(res.pack_operation_product_ids and rec.hanger_code.id):
                    if(rec.hanger_code.variasi_id.id):
                        for outPack in res.pack_operation_product_ids:
                            outPack.variasi_id = rec.hanger_code.variasi_id.id
                            outPack.qty_done = outPack.qty_done + ((outPack.qty_done * rec.hanger_code.shrinkage) / 100)
                            outPack.product_qty = outPack.product_qty + ((outPack.product_qty * rec.hanger_code.shrinkage) / 100)

                if(res.state!='assigned'):
                    #print "-----------------------------------------------"
                    res.action_assign()
        self.check_states = 'done'



    @api.multi
    def action_assign_manager(self):
        # if not self.is_after_check:
        #     raise UserError(_('Silahkan Klik button Check Stock terlebih dahulu.'))
        #stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',self.id)])
        if self.hanger_code.mlot_id:
            if self.hanger_code.is_order_pertama == True and self.hanger_code.mlot_id.state == 'approve_rnd':
                raise UserError('Silahkan Klik Button Check terlebih dahulu.')
        if self.is_mlot == False and self.notulen == False:
            raise UserError('Silahkan Klik tombol Notulen terlebih dahulu.')
        #for rec in stockPickingCheck:
        #    rec.action_assign()
        context = self.env.context
        seq_id = self.env['ir.sequence']
        # if context.get('is_work_order'):
        if self.is_work_order == True:
            for wo_id in self :
                code = ''
                if wo_id.type == 'dyeing' :
                    wo_id.name = seq_id.next_by_code('wo.dyeing')
                    code = 'D'
                elif wo_id.type == 'printing':
                    wo_id.name = seq_id.next_by_code('wo.printing')
                    code = 'P'
            for wo_id in self :
                no = 1
                for line in wo_id.order_line:
                    # line.batch = wo_id.name.split('/')[3] +  "-" +self.env['ir.sequence'].next_by_code('no.batch')
                    monthDict = {"01" : "A",
                                "02" : "B",
                                "03" : "C",
                                "04" : "D",
                                "05" : "E",
                                "06" : "F",
                                "07" : "G",
                                "08" : "H",
                                "09" : "I",
                                "10" : "J",
                                "11" : "K",
                                "12" : "L"}
                    bulanCreateKp = monthDict.get(datetime.now().strftime("%m"))
                    bulanWo  = wo_id.name.split('/')[2]
                    noUrutWo = wo_id.name.split('/')[3]
                    print '===============approve============'
                    print code + bulanCreateKp + bulanWo + noUrutWo
                    line.batch = code + bulanCreateKp + str(no) + '-' +bulanWo + noUrutWo
                    _logger.warning('='*40)
                    _logger.warning('ON APPROVE WORK ORDER')
                    _logger.warning( '-' +bulanWo + noUrutWo)
                    _logger.warning(line.batch)
                    _logger.warning('='*40)
                    no += 1
            self.create_planning_global()
            if self.is_mlot == False:
                self.hanger_code.write({'is_order_pertama':True})
        

        # self.action_confirm()

        stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',self.id)])
        for rec in stockPickingCheck:
            originWo = ' (' +  self.origin + ')'if self.origin else ''
            rec.origin = self.name + originWo
            rec.picking_type_id = 178
            rec.location_dest_id = self.env['stock.picking.type'].browse(178).default_location_dest_id.id
            
            if(rec.move_lines and self.hanger_code.id):
                if(self.hanger_code.variasi_id.id):
                    for outMove in rec.move_lines:
                        outMove.product_id = self.hanger_code.product_id.id
                        outMove.variasi_id = self.hanger_code.variasi_id.id
                        outMove.product_uom_qty = outMove.product_uom_qty + ((outMove.product_uom_qty * self.hanger_code.shrinkage) / 100)

            if(rec.pack_operation_product_ids and self.hanger_code.id):
                if(self.hanger_code.variasi_id.id):
                    for outPack in rec.pack_operation_product_ids:
                        outPack.product_id = self.hanger_code.product_id.id
                        outPack.variasi_id = self.hanger_code.variasi_id.id
                        outPack.qty_done = outPack.qty_done + ((outPack.qty_done * self.hanger_code.shrinkage) / 100)
                        outPack.product_qty = outPack.product_qty + ((outPack.product_qty * self.hanger_code.shrinkage) / 100)
                        # self.qty_request_greige = self.qty_process + ((self.qty_process * self.susut) / 100)


            if(rec.state!='assigned'):
                rec.action_assign()

                        
        #raise UserError('555555555555555555555555555')

        self.state         = 'confirm_wo'
        self.states_greige = 'approve'





    # ORIGINAL CODE 3 APRIL 2021
    # @api.multi
    # def action_assign_manager(self):
    #     # if not self.is_after_check:
    #     #     raise UserError(_('Silahkan Klik button Check Stock terlebih dahulu.'))
    #     stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',self.id)])
    #     if self.hanger_code.mlot_id:
    #         if self.hanger_code.is_order_pertama == True and self.hanger_code.mlot_id.state == 'approve_rnd':
    #             raise UserError('Silahkan Klik Button Check terlebih dahulu.')
    #     if self.is_mlot == False and self.notulen == False:
    #             raise UserError('Silahkan Klik tombol Notulen terlebih dahulu.')
    #     for rec in stockPickingCheck:
    #         rec.action_assign()
    #     context = self.env.context
    #     seq_id = self.env['ir.sequence']
    #     if context.get('is_work_order'):
    #         for wo_id in self :
    #             if wo_id.type == 'dyeing' :
    #                 wo_id.name = seq_id.next_by_code('wo.dyeing')
    #             elif wo_id.type == 'printing':
    #                 wo_id.name = seq_id.next_by_code('wo.printing')
    #         for wo_id in self :
    #             for line in wo_id.order_line:
    #                 line.batch = wo_id.name.split('/')[3] +  "-" +self.env['ir.sequence'].next_by_code('no.batch')
    #         self.create_planning_global()
    #         if self.is_mlot == False:
    #             self.hanger_code.write({'is_order_pertama':True})
    #     self.state         = 'confirm_wo'
    #     self.states_greige = 'approve'


    # @api.model
    # def default_get(self, fields):
    #     res = super(WorkOrder, self).default_get(fields)
    #     if res.get('type_wo') == 'stock':
    #         res['warehouse_id'] = 2
    #     return res

    # def _default_warehouse_id(self):
    #     res = super(WorkOrder, self)._default_warehouse_id()
    #     res = 2
    #     print '======_default_warehouse_id========'
    #     print res
    #     return res



    @api.onchange('type_wo')
    def _onchange_type_wo(self):
        print '==============='
        self.warehouse_id = 2
        if self.type_wo == 'stock':
            self.partner_id = 1
            self.sales_type = 'jual'
            print '================ffffffffff'
        else:
            self.partner_id = False
        #   self.sc_id = False


    @api.onchange('sc_id')
    def _onchange_sc_id(self):
        for rec in self:

            rec.partner_id       = rec.sc_id.partner_id.id
            rec.customer_code    = rec.sc_id.partner_code
            rec.piece_length_uom = rec.sc_id.piece_length_uom.id
            rec.sales_type       = rec.sc_id.sales_type
            rec.lebar_finish     = rec.sc_id.lebar_finish
            rec.gramasi_finish   = rec.sc_id.gramasi_finish
            rec.potongan_pinggir = rec.sc_id.potongan_pinggir
            rec.process          = rec.sc_id.process
            rec.grading          = rec.sc_id.grading
            rec.max_joint_pieces = rec.sc_id.max_joint_pieces
            rec.piece_length     = rec.sc_id.piece_length
            rec.packing          = rec.sc_id.packing
            rec.accessories_id   = rec.sc_id.accessories_id
            rec.hang_tag_id      = rec.sc_id.hang_tag_id
            rec.process_id       = rec.sc_id.process.id
            rec.uom_id           = rec.sc_id.qty_sc_uom_id.id
            rec.hanger_greige    = rec.sc_id.td_id.product_id.id
            rec.hanger_code      = rec.sc_id.td_id.id
            rec.greige_code      = rec.sc_id.td_id.greige_code





            # ----- pengisian data type berdasarkan data sale_contract.category_id
            if(rec.sc_id.category_id.id==1 or rec.sc_id.category_id.id==2):
                rec.type = 'dyeing'

            if(rec.sc_id.category_id.id==3 or rec.sc_id.category_id.id==4):
                rec.type = 'printing'





    # ----------- ORIGINAL CODE YUGI 19 FEBRUARI 2021
    @api.onchange('type')
    def _compute_type(self):
        self.order_line = False
        if self.type == 'dyeing':
            self.strike_off_id = False
            self.design_id = False
        elif self.type == 'printing':
            self.labdip_id = False



    # @api.onchange('type')
    # def _compute_type(self):
    #     self.order_line = False
    #     if self.type == 'dyeing':
            

    #         return {
    #             'value':{
    #                 'strike_off_id':False,
    #                 'sc_id':False,
    #             },
    #             'domain':{
    #                 'sc_id':[('category_id','in',[1,2])]
    #             }
    #         }



    #     elif self.type == 'printing':
            
    #         return {
    #             'value':{
    #                 'labdip_id':False,
    #                 'sc_id':False,
    #             },
    #             'domain':{
    #                 'sc_id':[('category_id','in',[3,4])]
    #             }
    #         }




    # ORIGINAL CODE 25 FEBRUARI 2021
    @api.onchange('strike_off_id')
    def _onchange_strike_ood_id(self):
        self.design_id = self.strike_off_id.design_id.id

    
    # @api.onchange('sc_id')
    # def onchange_sc_id(self):
    #     td_id = self.sc_id.td_id.id
    #     print("======== onchange id")
    #     print(td_id)
    #     res = {}
    #     res['domain'] = {'hanger_code': [('id','in', td_id)]}
    #     return res
    
    @api.multi
    def action_cancel(self):
        self.state = 'draft_wo'
        self.check_states = ''

    # def domain_hanger_code(self):
    #     td_ids = self.sc_id.td_ids.ids
    #     sc_id = self.sc_id.id
    #     print("=========== domain_hanger_code")
    #     print td_ids
    #     print(sc_id)
    #     print(self.id)
    #     return td_ids

    @api.onchange('labdip_id')
    def _onchange_labdip_id(self):
        if self.labdip_id :
            if not self.hanger_code:
                raise ValidationError(_("Field Hanger Code masih kosong !"))

                if not self.product_id :
                    raise ValidationError(_("Field Product di form test development - "+ self.hanger_code.name+" masih kosong !"))

            new_lines = self.env['sale.order.line']

            for warna in self.labdip_id.warna_ids:
                data = {
                    'product_id':self.product_id.id,
                    'color' : warna.warna_id.id,
                    'color_no' : warna.no_warna,
                    'labdip_id' : self.labdip_id,
                    'uom':self.contract_id.qty_order_uom.id,

                }
                new_line = new_lines.new(data)
                new_lines += new_line
            self.order_line = new_lines

    @api.multi
    def load_warna(self):
        if not self.order_line:
            for obj in self.strike_off_id.detail_ids:
                detail_id= self.order_line.create({
                    'order_id'      : self.id,
                    'sto_line_id'   : obj.id,
                    'product_id'    : self.contract_id.product_id.id,
                    'color'         : obj.name.id,
                    'color_no'      : obj.no_warna,
                    })



    # ORIGINAL CODE 3 APRIL 2021
    # @api.model
    # def create(self, values):
    #     print '=========== create so'
    #     print values


    #     context = self.env.context
    #     if context.get('is_work_order'):
    #         values['state'] = 'draft_wo'
    #         values['name'] = 'New'
    #         values['is_work_order'] = True
    #         values['warehouse_id'] = 2
    #         # self.pop_up_warning()
    #     else:
    #         values['name'] = 'New'
    #     res = super(WorkOrder, self).create(values)


    #     for rec in res:
    #         if('strike_off_id' in values):
    #             rec.strike_off_id = values['strike_off_id']            


    #     return res




    @api.model
    def create(self, values):
        print '=========== create so'
        print values


        context = self.env.context
        if context.get('is_work_order'):
            values['state'] = 'draft_wo'
            values['name'] = 'New'
            values['is_work_order'] = True
            values['warehouse_id'] = 2
            a = values.get('order_line')
            if len(a) > 6:
                raise ValidationError("Anda hanya diperbolehkan mengisi data WO line 6 data saja!!!")
            total_product_uom_qty = sum(map(lambda x: x[2]['product_uom_qty'], a))
            if self.env['sale.contract'].browse(values.get('sc_id')).qty_sc < total_product_uom_qty:
                raise ValidationError("Mohon maaf total quantity WO Line tidak diperbolehkan melebihi quantity Sale Contract")
            # self.pop_up_warning()
        else:
            values['name'] = 'New'
        res = super(WorkOrder, self).create(values)


        for rec in res:
            if('strike_off_id' in values):
                rec.strike_off_id = values['strike_off_id']            


        return res

    @api.multi
    def write(self, values):
        context = self.env.context
        if values.get('order_line'):
                    if len(values.get('order_line')) > 6:
                        raise UserError("Anda hanya diperbolehkan mengisi data WO line 6 data saja!!!")
        return super(WorkOrder, self).write(values)



    # def pop_up_warning(self):
    #     # if self.hanger_code.is_order_pertama == True and self.hanger_code.mlot_id.state != 'approve':
    #     #         print '===action==='
    #     #         action = self.env.ref('work_order.pop_up_warning_action').read()[0]
    #     #         print action
    #     #         asjasjdasda
    #     #         return action            
    #     action = self.env.ref('work_order.pop_up_warning_action').read()[0]
    #     print '========sadasa=========='
    #     print action
    #     return action

    @api.multi
    def update_flowproses(self):
        td_id = self.hanger_code
        kp_ids = self.env['kartu.proses'].sudo().search([('so_id','=',self.id)]).filtered(lambda x:x.state == 'draft')
        for kp in kp_ids:
            self._cr.execute("DELETE from kartu_proses_flow_proses where kp_id = %s"%(kp.id))
            kp.sudo().write({
                "hanger_code": td_id.id,
                # 'proses_ids': [(6, 0, td_id.flowproses_ids )],
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
                            'gramasi_result':proses.gramasi_result,'weight_reduce':proses.weight_reduce,'keterangan':proses.keterangan,
                            'process_type':proses.process_type.id,'density':proses.density,'no_urut_actual':proses.no_urut_actual,
                            'parameter_ids': [[0, 0, {'name':proses.name,'description': param.description, 'state': param.state, 'amount': param.amount, 'td_id': proses.td_id.id, 'parameter_id': param.parameter_id.id,'no_urut': param.no_urut, 'var_proses': param.var_proses, 'nilai': param.nilai, 'uom': param.uom.id}] for param in proses.parameter_ids],
                            'chemical_ids': [[0, 0, {'name':chemical.name,'description': chemical.description, 'state': chemical.state, 'amount': chemical.amount, 'td_id': proses.td_id.id, 'qty': chemical.qty, 'qty_be': chemical.qty_be,'no_urut': chemical.no_urut, 'var_proses': chemical.var_proses, 'product_id': chemical.product_id.id, 'uom_id': chemical.uom_id.id}] for chemical in proses.chemical_ids],
                            'state_parent':proses.state_parent}] for proses in td_id.flowproses_ids ],
            })
    
    
    
    

class WorkOrderDetail(models.Model):
    _inherit = 'sale.order.line'

    color = fields.Many2one('makloon.warna', String='Color')
    color_no_labdip = fields.Many2one('labdip.warna','Color No')
    color_no   = fields.Char(string='Color no')
    partner_id = fields.Many2one('res.partner', string='Partner')
    labdip_id = fields.Many2one('labdip','Labdip No',)
    qty_weight = fields.Float('Qty (KG)',)
    qty_length = fields.Float('Qty Length (YARDS)', compute="_compute_konversi", invers=True)
    uom = fields.Many2one('product.uom', String='UOM')
    description = fields.Char('Description')
    kp_ids = fields.One2many('kartu.proses','so_line_id',string='Kartu Proses')
    strikeoff_id = fields.Many2one('strikeoff', related="order_id.strike_off_id", string='Strike Off')
    sto_line_id = fields.Many2one('strikeoff.detail', string='Strike Line')
    batch = fields.Char(string='Batch')
    total_batch = fields.Float(string='Total Batch')
    qty_pcs = fields.Integer('Quantity Pcs')
    qty_meter = fields.Float('Quantity Meter', compute="_compute_konversi_mtr")
    meter_conv = fields.Float('Meter Conversion')
    mesin_id = fields.Char('Mesin Printing')
    wip_status = fields.Char('Wip Status')
    wip_date = fields.Date('Wip Date')
    wip_days = fields.Date('Wip Days')
    remarks = fields.Char('Remarks')
    kp_existed = fields.Boolean('Is KP existed?', default=False)
    contract_id = fields.Many2one(related='order_id.contract_id', store=True, string='No SC')
    wo_date = fields.Date(related='order_id.wo_date', store=True, string='Tanggal WO')
    delivery_date = fields.Date(related='order_id.delivery_date', required=True, string='Delivery Date')

    kp_wo_line_ids = fields.One2many('kartu.proses','sodet_id',string='Kartu Proses')

    status_permartaian = fields.Selection(opsi_permartaian,compute="get_status_permartaian",store=True)
    status_pengiriman  = fields.Selection(opsi_pengiriman,compute="get_status_pengiriman",store=True)
    image = fields.Binary(string='Image', related='order_id.strike_off_id.image')
    color_makloon_id   = fields.Many2one('makloon.warna',string='Color',)

    show_keterangan = fields.Boolean(string="Tampilkan Keterangan", default=False)
    keterangan = fields.Text(string='Keterangan')

    show_note = fields.Boolean(string="Tampilkan Note", default=False)
    ref_note = fields.Text(related='order_id.note', string='WO Note')

    ref_wo = fields.Char(related='order_id.origin', string='WO Ref')
    # color_labdip_id    = fields.Many2one('makloon.warna',string='Color',)
    # color_strikeoff_id = fields.Many2one('makloon.warna', string='Color',)
    type_sc = fields.Selection(
        selection=[
            ('dyeing', 'Work Order Dyeing'),
            ('printing', 'Work Order Printing'),
            ],
        string='Type',)
    qty_minimum                = fields.Float(string='Qty Minimum',)
    color_customer_id          = fields.Many2one('makloon.warna', string='Color Customer')
    variasi_id                 = fields.Many2one('tj.stock.variasi', string='Variation Name', related="order_id.hanger_code.variasi_id")
    greige_code                = fields.Char(string='Greige Code', related="order_id.hanger_code.greige_code")
    quantity_roll = fields.Float(string='Roll')

    qty_process = fields.Float('Qty Proses', compute='getQtySummary', store=True)
    qty_remaining =  fields.Float('Qty Sisa', compute='getQtySummary', store=True)
    

    def toggle_keterangan(self):
        for record in self:
            record.show_keterangan = not record.show_keterangan

    def toggle_note(self):
        for record in self:
            record.show_note = not record.show_note
    
    @api.multi
    def toggle_all_keterangan(self):
        """Toggle semua note (True -> False atau False -> True)."""
        records = self.search([])
        print("Records to update (toggle_all_note): {}".format(records))
        
        toggle_to = not any(records.mapped('show_keterangan'))
        print("Toggling all records to show_keterangan={}".format(toggle_to))
        
        for record in records:
            record.show_keterangan = toggle_to
        
        print("All records have been updated with show_keterangan={}.".format(toggle_to))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def toggle_all_note(self):
        """Toggle semua note (True -> False atau False -> True), lalu reload view."""
        records = self.search([])
        toggle_to = not any(records.mapped('show_note'))
        print("Toggling all records to show_note={}".format(toggle_to))
        
        for record in records:
            record.show_note = toggle_to
        
        print("All records have been updated with show_note={}.".format(toggle_to))
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('color_no_labdip')
    def _onchange_color_no(self):
        context = self.env.context
        if context.get('type_wo') != 'stock':
            if self.labdip_id.id == False and self.color_makloon_id.id == False and self.strikeoff_id.id == False:
                # LabdipWarnaObj = self.env['labdip.warna'].search([('name','=',self.color_no)], limit=1)
                # self.color_makloon_id = LabdipWarnaObj.warna_id.id
                # self.labdip_id        = LabdipWarnaObj.labdip_id.id
                self.color_makloon_id = self.color_no_labdip.warna_id.id
                self.labdip_id        = self.color_no_labdip.labdip_id.id
    


    # ORIGINAL CODE 3 APRIL 2021
    # @api.onchange('color_makloon_id')
    # def _onchange_color_makloon(self):
    #     context = self.env.context
    #     if context.get('is_wo'):
    #         self.name     = self.color_makloon_id.name
    #         if self.labdip_id.id:
    #             LabdipWarnaObj = self.env['labdip.warna'].search([('labdip_id','=',self.labdip_id.id),('warna_id','=',self.color_makloon_id.id)], limit=1)
    #             self.color_no_labdip = LabdipWarnaObj.id

    #         self.product_id = self.order_id.product_id.id


    @api.onchange('color_makloon_id')
    def _onchange_color_makloon(self):
        context = self.env.context
        if context.get('is_wo'):
            self.name     = self.color_makloon_id.name
            if self.labdip_id.id:
                LabdipWarnaObj = self.env['labdip.warna'].search([('labdip_id','=',self.labdip_id.id),('warna_id','=',self.color_makloon_id.id)], limit=1)
                self.color_no_labdip = LabdipWarnaObj.id


            if(self.order_id.hanger_code.product_id.id):
                self.product_id = self.order_id.hanger_code.product_id.id
            else:
                self.product_id = self.order_id.product_id.id



    # ORIGINAL CODE 3 APRIL 2021
    # @api.onchange('labdip_id')
    # def domain_color(self):
    #     context = self.env.context
    #     self.type_sc = self.order_id.type
    #     print '=========domain color==========='
    #     print context.get('type_wo')
    #     if(context.get('type_wo') != 'stock'):
    #         print '=======THIS WO ORDER======='
    #         print self.partner_id.id
    #         print context.get('product')
    #         LabdipWarnaObj = self.env['labdip.warna'].search([('labdip_id','=',self.labdip_id.id)])
    #         # StrikeOffLineObj = self.env['strikeoff.detail'].search([('id_sof','=',self.strikeoff_id.id)])
    #         my_id = []
    #         if self.labdip_id.id:
    #             for rec in LabdipWarnaObj:
    #                 my_id.append(rec.warna_id.id)   
    #         return {
    #             'domain':
    #                 {
    #                     'color_makloon_id': [('id', 'in', my_id)],
    #                     'labdip_id': [('partner_id','=',self.partner_id.id),('product_name','=',context.get('product'))],
    #                     'color_no_labdip' :[('partner_id','=',self.partner_id.id),('product_id','=',context.get('product'))],
    #                 }
    #             }



    @api.onchange('labdip_id')
    def domain_color(self):
        context = self.env.context
        self.type_sc = self.order_id.type
        #print '=========domain color==========='
        #print context.get('type_wo')
        if(context.get('type_wo') != 'stock'):
            
            # print '=======THIS WO ORDER======='
            # print self.partner_id.id
            # print context.get('product')
            

            tmpProduct = context.get('product')
            # if(self.order_id.hanger_code.product_id.id):
            #     tmpProduct = self.order_id.hanger_code.product_id.id


            #print " TMP PRODUCT :::: ", tmpProduct
            LabdipWarnaObj = self.env['labdip.warna'].search([('labdip_id','=',self.labdip_id.id)])
            # StrikeOffLineObj = self.env['strikeoff.detail'].search([('id_sof','=',self.strikeoff_id.id)])
            my_id = []
            if self.labdip_id.id:
                for rec in LabdipWarnaObj:
                    my_id.append(rec.warna_id.id)   
            return {
                'domain':
                    {
                        'color_makloon_id': [('id', 'in', my_id)],
                        'labdip_id': [('partner_id','=',self.partner_id.id),('product_name','=',tmpProduct)],
                        'color_no_labdip' :[('partner_id','=',self.partner_id.id),('product_id','=',tmpProduct)],
                    }
                }


    @api.onchange('strikeoff_id')
    def domain_color_strike_off(self):
        context = self.env.context
        design_id = context.get('design_id')
        domain = False
        if(self.strikeoff_id):
            #print "-----------"
            
            StrikeOffLineObj = self.env['strikeoff.detail'].search([('id_sof','=',self.strikeoff_id.id)])
            id_sd = []
            
            for rec in StrikeOffLineObj:
                id_sd.append(rec.name.id)
            
            domain = { 'domain': { 'color_makloon_id': [('id', 'in', id_sd)]},}
        elif design_id != False and self.strikeoff_id.id == False:
            # colorId = self.env['makloon.design.line'].search([('order_id','=',design_id)]).color_id.mapped('id')
            idColor = []
            makloonDesignObj = self.env['makloon.design'].browse(design_id).makloon_design_line
            for rec in makloonDesignObj:
                idColor.append(rec.color_id.id)
            domain = { 'domain': { 'color_makloon_id': [('id', 'in', idColor)]},}
        return domain
    
    
    
    # ORIGINAL CODE 16 MARET 2001
    # @api.depends('qty_weight')
    # def _compute_konversi(self):
    #     for rec in self:
    #         if rec.order_id.hanger_code.gramasi_greige !=0 and rec.order_id.hanger_code.lebar_greige !=0:
    #             meter = rec.qty_weight * 1000 / rec.order_id.hanger_code.gramasi_greige / rec.order_id.hanger_code.lebar_greige * 100
    #             rec.qty_length = meter / 0.9144



    @api.depends('qty_weight')
    def _compute_konversi(self):
        for rec in self:
            rec.qty_length = 0



    # def _inverse_weight(self):
    #     for rec in self:
    #         if rec.qty_length:
    #             rec.qty_weight = rec.qty_length * rec.order_id.hanger_code.gramasi_greige * rec.order_id.hanger_code.lebar_greige * 0.9144 / 100 / 1000

    @api.depends('qty_length')
    def _compute_konversi_mtr(self):
        for rec in self:
            if rec.qty_length:
                rec.qty_meter =  rec.qty_length * 0.9144
    
    # def _inverse_mtr(self):
    #     for rec in self:
    #         if rec.qty_meter:
    #             rec.qty_length =  rec.qty_meter / 0.9144

    @api.depends('qty_process')
    @api.multi
    def get_status_permartaian(self):
        for obj in self:
            if obj.qty_process == obj.product_uom_qty :
                obj.status_permartaian = 'done'
            elif obj.qty_process < obj.product_uom_qty and obj.qty_process > 0 :
                obj.status_permartaian = 'in_progress'
            elif obj.qty_process == 0:
                obj.status_permartaian = 'not_worked'

    @api.depends('qty_delivered')
    @api.multi
    def get_status_pengiriman(self):
        for obj in self:
            if obj.qty_delivered == obj.product_uom_qty :
                obj.status_pengiriman = 'done'
            elif obj.qty_delivered < obj.product_uom_qty and obj.qty_delivered > 0 :
                obj.status_pengiriman = 'partial'
            elif obj.qty_delivered == 0:
                obj.status_pengiriman = 'not_delivered'

    @api.onchange('color')
    def onchange_color(self):
        domain = {}
        if self.order_id.strike_off_id :
            color_ids = self.order_id.strike_off_id.mapped('detail_ids.name')
            print("\n color_ids",color_ids)
            print("\n self.color", self.color)
            if self.color.id not in color_ids.ids :
                self.color = False
            domain['color'] = [('id','in',color_ids.ids)]
        return {'domain':domain}

    @api.depends('kp_wo_line_ids','product_uom_qty')
    @api.multi
    def getQtySummary(self):
        for obj in self:
            obj.qty_process = sum(obj.kp_wo_line_ids.filtered(lambda x:x.state != 'cancel').mapped('qty_process'))
            obj.qty_remaining = obj.product_uom_qty - obj.qty_process

    @api.onchange('product_uom_qty')
    def onChangeProductUomQTy(self):
        print '========onChangeProductUomQTy'
        context = self.env.context
        print context
        if context.get('is_work_order'):
            self.product_uom = context.get('default_product_uom')
        if context.get('default_qty_minimum'):
            for a in self:
                if a.product_uom_qty:
                    if a.product_uom_qty < context.get('default_qty_minimum'):
                        raise UserError(_('Mohon maaf quantity tidak boleh kurang dari %s') % (context.get('default_qty_minimum')))
    


        if context.get('is_wo'):
            if(self.order_id.strike_off_id):

                listColor = []
                if(len(self.order_id.strike_off_id.detail_ids)>0):
                    for recWarna in self.order_id.strike_off_id.detail_ids:
                        listColor.append(recWarna.name.id)

                #print " >>>>>>>>>> DAFTAR WARNA ",listColor

                return {
                    'domain':{
                        'color_makloon_id':[('id', 'in', listColor)],
                    }
                }



    @api.onchange('color_makloon_id')
    def domain_product_uom(self):
        return {
            'domain':
                {
                    'product_uom': [('id', 'in', [106,77,3])]
                },
        }
    

        # if context.get('is_wo'):
        #     if(self.order_id.strike_off_id):

        #         listColor = []
        #         if(len(self.order_id.strike_off_id.detail_ids)>0):
        #             for recWarna in self.order_id.strike_off_id.detail_ids:
        #                 listColor.append(recWarna.name.id)

        #         #print " >>>>>>>>>> DAFTAR WARNA ",listColor

        #         return {
        #             'domain':{
        #                 'color_makloon_id':[('id', 'in', listColor)],
        #             }
        #         }


    @api.model
    def create(self, values):
        # Add code here
        res = super(WorkOrderDetail, self).create(values)
        context = self.env.context
        if context.get('is_wo'):
            productUomQty = values.get('product_uom_qty')
            compare = float_compare(values.get('qty_minimum'), productUomQty, precision_digits=2)
            if compare == 1:
                raise UserError(_('Mohon maaf quantity tidak boleh kurang dari %s') % (values.get('qty_minimum') ))     
            # if context.get('is_work_order'):
            #     if values.get('qty_minimum'):
            #         if productUomQty < values.get('qty_minimum'):
                        # raise UserError(_('Mohon maaf quantity tidak boleh kurang dari %s') % (values.get('qty_minimum') ))     
        return res

    @api.model
    def default_get(self, fields):
        res = super(WorkOrderDetail,self).default_get(fields)
        context = self.env.context
        if context.get('is_wo'):
            res['product_uom_qty'] = context.get('default_qty_minimum')
        return res



    
    # ==== OVERRIDE BASE ODOO
    @api.onchange('product_uom_qty', 'product_uom', 'route_id', 'product_id')
    def _onchange_product_id_check_availability(self):
        res = super(WorkOrderDetail, self)._onchange_product_id_check_availability()
        res = {}
        # if not self.product_id or not self.product_uom_qty or not self.product_uom:
        #     self.product_packaging = False
        #     return {}
        # if self.product_id.type == 'product':
        #     precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        #     product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
            
        #     # --- begin pengecekan dari work order
        #     context = self.env.context
        #     if(context.get('is_wo')!=1):
        #         if float_compare(self.product_id.virtual_available, product_qty, precision_digits=precision) == -1:
        #             is_available = self._check_routing()
        #             if not is_available:
        #                 warning_mess = {
        #                     'title': _('Not enough inventory!'),
        #                     'message' : _('You plan to sell %s %s but you only have %s %s available!\nThe stock on hand is %s %s.') % \
        #                         (self.product_uom_qty, self.product_uom.name, self.product_id.virtual_available, self.product_id.uom_id.name, self.product_id.qty_available, self.product_id.uom_id.name)
        #                 }
        #                 return {'warning': warning_mess}
        return res



class NotulenWizard(models.TransientModel):
    _name = 'notulen.wizard'

    #name = fields.Char(string='Notulen', size=20, required=True)
    name = fields.Text(string='Notulen', required=True)

    def action_update_notulen(self):

        if(len(self.name) < 5):
            raise UserError('Jumlah karakter isian notulen harus lebih besar dari 5 karakter')


        ids_to_change = self._context.get('active_ids')
        workOrderObj = self.env['sale.order'].browse(ids_to_change).write({
            'notulen' : self.name,
            'is_notulen' : True,
            'check_states' : 'approve_rnd',
        })
        # 1. Run another function
        # doc_ids.set_open()

        # 2. Modify selected Document
        # doc_ids.write(
        #     {
        #         'state' : 'open'
        #     }
        # )



class SaleOrderSummaryRakVariasi(models.Model):
    _name = 'sale.order.rak.variasi'

    order_id = fields.Many2one('sale.order',ondelete="cascade")
    product_id = fields.Many2one('product.product', string='Greige Name')
    variasi_id = fields.Many2one('tj.stock.variasi', string='Variasi')

    variasi_name = fields.Char(related='variasi_id.name', string='Variasi Name')
    greige_code = fields.Char(related='variasi_id.code', string='Greige Code')
    balance_qty = fields.Float(string='balance_qty')
    
    balance_pcs = fields.Float(string='balance_pcs')
    




class SaleOrderRakVariasiWizard(models.TransientModel):
    _name = 'sale.order.rak.variasi.wizard'

    inventory_id = fields.Many2one('stock.inventory', string='Inventory Adjustment',required=True)
    location_id  = fields.Many2one('stock.location', 'Location', required=True)    
    date_start   = fields.Datetime("Start Date",required=True, default=lambda *a: time.strftime("%Y-%m-%d"))
    date_end     = fields.Datetime("End Date", required=True, default=lambda *a: time.strftime("%Y-%m-%d"))
    date_opname = fields.Datetime(related='inventory_id.date', string="Date Opname")

    
    def action_calculate_summary_rak_variasi(self):
        
        
        order_id = self._context.get('active_ids')[0]
        #product_id = self.env.context.get('product_id')
        
        hanger_code = self.env.context.get('hanger_code')
        id_inventory = self.inventory_id.id
        id_location = self.location_id.id
        date_opname = self.date_opname
        date_start = self.date_start
        date_end = self.date_end
        

        product_id = False
        variasi_id = False
        tdPool = self.env['test.development'].search([('id','=',int(hanger_code))])
        for tdData in tdPool:
            if(tdData.product_id.id!=False):
                product_id = tdData.product_id.id
            
            if(tdData.variasi_id.id!=False):
                variasi_id = tdData.variasi_id.id

        

        query1 = """
                DELETE FROM sale_order_rak_variasi where order_id=%s
        """%(order_id)
        self._cr.execute(query1)
        self._cr.commit()


        query = ""
        if(variasi_id==False):
            query = """
                INSERT INTO sale_order_rak_variasi (order_id,product_id,variasi_id,balance_qty,balance_pcs) 
                (
                    select %s,
                    product_id, variasi_id, 
                    sum(saldo_awal_qty) + sum(terima_qty) + sum(retur_terima_qty) - sum(keluar_qty) - sum(retur_keluar_qty) + sum(adj_qty) as balance_qty,
                    sum(saldo_awal_pcs) + sum(terima_pcs) + sum(retur_terima_pcs) - sum(keluar_pcs) - sum(retur_keluar_pcs) + sum(adj_pcs) as balance_pcs
                    From (
                        select b.id,b.product_id,b.prod_lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,b.product_qty as saldo_awal_qty, 1 as saldo_awal_pcs, 0 as saldo_awal_kg, 0 as saldo_awal_yard, 0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_inventory a , stock_inventory_line b where a.id=%s  and  a.id=b.inventory_id and b.location_id=%s and b.product_id=%s
                        union
                        select row_number() OVER () as id,
                        product_id, lot_id,rak_id , variasi_id , product_uom_id,
                        sum(saldo_awal_qty) + sum(terima_qty) + sum(retur_terima_qty) - sum(keluar_qty) - sum(retur_keluar_qty) + sum(adj_qty) as saldo_awal_qty,
                        sum(saldo_awal_pcs) + sum(terima_pcs) + sum(retur_terima_pcs) - sum(keluar_pcs) - sum(retur_keluar_pcs) + sum(adj_pcs) as saldo_awal_pcs,
                        sum(saldo_awal_kg) + sum(terima_kg) - sum(keluar_kg) as saldo_awal_kg,
                        sum(saldo_awal_yard) + sum(terima_yard) - sum(keluar_yard) as saldo_awal_yard,
                        sum(saldo_awal_meter) + sum(terima_meter) - sum(keluar_meter) as saldo_awal_meter,
                        
                        0 as terima_qty,0 as terima_pcs,0 as terima_kg,0 as terima_yard,0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs,0 as terima_kg,0 as terima_yard,0 as terima_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs
                        fRom (                   
                            select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, c.qty as terima_qty,1 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b, stock_pack_operation_lot c where a.min_date > '%s' and a.min_date < '%s'  and  a.id=b.picking_id and b.id=c.operation_id and a.location_dest_id=%s and a.state='done' and b.product_id=%s
                            union
                            select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, c.qty as keluar_qty, 1 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b, stock_pack_operation_lot c where a.min_date > '%s' and a.min_date < '%s'  and  a.id=b.picking_id and b.id=c.operation_id and a.location_id=%s and a.state='done' and b.product_id = %s
                            ) as a group by product_id, lot_id, rak_id, variasi_id , product_uom_id
                        union
                        select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, c.qty as terima_qty, 1 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b , stock_pack_operation_lot c where a.min_date >= '%s' and a.min_date <= '%s' and a.id=b.picking_id and b.id=c.operation_id and a.location_dest_id=%s and a.state='done' and b.product_id=%s
                        union
                        select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, c.qty as keluar_qty, 1 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b , stock_pack_operation_lot c where a.min_date >= '%s' and a.min_date <= '%s' and a.id=b.picking_id and b.id=c.operation_id and a.location_id=%s and a.state='done' and b.product_id=%s                 
                        ) as a 
                        where
                        (
                            saldo_awal_qty > 0
                            OR saldo_awal_kg > 0  
                            OR saldo_awal_yard > 0 
                            OR saldo_awal_meter > 0 
                            OR saldo_awal_pcs > 0
                            OR terima_qty > 0 
                            OR terima_kg > 0 
                            OR terima_yard > 0 
                            OR terima_meter > 0 
                            OR terima_pcs > 0
                            OR retur_terima_qty > 0 
                            OR retur_terima_pcs > 0
                            OR keluar_qty > 0
                            OR keluar_kg > 0 
                            OR keluar_yard > 0 
                            OR keluar_meter > 0 
                            OR keluar_pcs > 0
                            OR retur_keluar_qty > 0 
                            OR retur_keluar_pcs > 0 
                            OR adj_qty > 0 
                            OR adj_pcs > 0
                        )

                        group by rak_id,product_id, variasi_id , product_uom_id

                )

                """%(order_id,id_inventory,id_location,product_id,
                    date_opname,date_start,id_location,product_id,
                    date_opname,date_start,id_location,product_id,
                    date_start,date_end,id_location,product_id,
                    date_start,date_end,id_location,product_id)
        else:


            query = """
                INSERT INTO sale_order_rak_variasi (order_id,product_id,variasi_id,balance_qty,balance_pcs) 
                (
                    select %s,
                    product_id, variasi_id, 
                    sum(saldo_awal_qty) + sum(terima_qty) + sum(retur_terima_qty) - sum(keluar_qty) - sum(retur_keluar_qty) + sum(adj_qty) as balance_qty,
                    sum(saldo_awal_pcs) + sum(terima_pcs) + sum(retur_terima_pcs) - sum(keluar_pcs) - sum(retur_keluar_pcs) + sum(adj_pcs) as balance_pcs
                    From (
                        select b.id,b.product_id,b.prod_lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,b.product_qty as saldo_awal_qty, 1 as saldo_awal_pcs, 0 as saldo_awal_kg, 0 as saldo_awal_yard, 0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_inventory a , stock_inventory_line b where a.id=%s  and  a.id=b.inventory_id and b.location_id=%s and b.product_id=%s and b.variasi_id=%s
                        union
                        select row_number() OVER () as id,
                        product_id, lot_id,rak_id , variasi_id , product_uom_id,
                        sum(saldo_awal_qty) + sum(terima_qty) + sum(retur_terima_qty) - sum(keluar_qty) - sum(retur_keluar_qty) + sum(adj_qty) as saldo_awal_qty,
                        sum(saldo_awal_pcs) + sum(terima_pcs) + sum(retur_terima_pcs) - sum(keluar_pcs) - sum(retur_keluar_pcs) + sum(adj_pcs) as saldo_awal_pcs,
                        sum(saldo_awal_kg) + sum(terima_kg) - sum(keluar_kg) as saldo_awal_kg,
                        sum(saldo_awal_yard) + sum(terima_yard) - sum(keluar_yard) as saldo_awal_yard,
                        sum(saldo_awal_meter) + sum(terima_meter) - sum(keluar_meter) as saldo_awal_meter,
                        
                        0 as terima_qty,0 as terima_pcs,0 as terima_kg,0 as terima_yard,0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs,0 as terima_kg,0 as terima_yard,0 as terima_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs
                        fRom (                   
                            select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, c.qty as terima_qty,1 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b, stock_pack_operation_lot c where a.min_date > '%s' and a.min_date < '%s'  and  a.id=b.picking_id and b.id=c.operation_id and a.location_dest_id=%s and a.state='done' and b.product_id=%s and b.variasi_id=%s
                            union
                            select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, c.qty as keluar_qty, 1 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b, stock_pack_operation_lot c where a.min_date > '%s' and a.min_date < '%s'  and  a.id=b.picking_id and b.id=c.operation_id and a.location_id=%s and a.state='done' and b.product_id = %s and b.variasi_id=%s
                            ) as a group by product_id, lot_id, rak_id, variasi_id , product_uom_id
                        union
                        select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, c.qty as terima_qty, 1 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, 0 as keluar_qty, 0 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b , stock_pack_operation_lot c where a.min_date >= '%s' and a.min_date <= '%s' and a.id=b.picking_id and b.id=c.operation_id and a.location_dest_id=%s and a.state='done' and b.product_id=%s and b.variasi_id=%s
                        union
                        select c.id,b.product_id,c.lot_id,COALESCE (NULLIF (b.rak_id,1),1) as rak_id,COALESCE (NULLIF (b.variasi_id,5778),5778) as variasi_id,COALESCE (NULLIF (b.product_uom_id,1),1) as product_uom_id,0 as saldo_awal_qty,0 as saldo_awal_pcs,0 as saldo_awal_kg,0 as saldo_awal_yard,0 as saldo_awal_meter, 0 as terima_qty,0 as terima_pcs, 0 as terima_kg, 0 as terima_yard, 0 as terima_meter, 0 as retur_terima_qty, 0 as retur_terima_pcs, c.qty as keluar_qty, 1 as keluar_pcs, 0 as keluar_kg, 0 as keluar_yard, 0 as keluar_meter, 0 as retur_keluar_qty, 0 as retur_keluar_pcs, 0 as adj_qty, 0 as adj_pcs  from stock_picking a , stock_pack_operation b , stock_pack_operation_lot c where a.min_date >= '%s' and a.min_date <= '%s' and a.id=b.picking_id and b.id=c.operation_id and a.location_id=%s and a.state='done' and b.product_id=%s and b.variasi_id=%s                 
                        ) as a 
                        where
                        (
                            saldo_awal_qty > 0
                            OR saldo_awal_kg > 0  
                            OR saldo_awal_yard > 0 
                            OR saldo_awal_meter > 0 
                            OR saldo_awal_pcs > 0
                            OR terima_qty > 0 
                            OR terima_kg > 0 
                            OR terima_yard > 0 
                            OR terima_meter > 0 
                            OR terima_pcs > 0
                            OR retur_terima_qty > 0 
                            OR retur_terima_pcs > 0
                            OR keluar_qty > 0
                            OR keluar_kg > 0 
                            OR keluar_yard > 0 
                            OR keluar_meter > 0 
                            OR keluar_pcs > 0
                            OR retur_keluar_qty > 0 
                            OR retur_keluar_pcs > 0 
                            OR adj_qty > 0 
                            OR adj_pcs > 0
                        )

                        group by rak_id,product_id, variasi_id , product_uom_id

                )

                """%(order_id,id_inventory,id_location,product_id,variasi_id,
                    date_opname,date_start,id_location,product_id,variasi_id,
                    date_opname,date_start,id_location,product_id,variasi_id,
                    date_start,date_end,id_location,product_id,variasi_id,
                    date_start,date_end,id_location,product_id,variasi_id)


        self._cr.execute(query)
        


















    # @api.multi
    # def open_wizard_create_kp(self):
    #     action = self.env.ref('work_order.action_wizard_create_kp')
    #     return {
    #         'name': action.name,
    #         'help': action.help,
    #         'type': action.type,
    #         'view_type': action.view_type,
    #         'view_mode': action.view_mode,
    #         'target': 'new',
    #         'res_model': action.res_model,
    #         'domain': [],
    #         'context':{'default_so_line_id':self.id}
    #     }



    # @api.multi
    # def create_kartu_proses(self):
    #     self.ensure_one()
    #     kp_obj = self.env['kartu.proses']
    #     data = {
    #             "type_kp": 'd',
    #             "product_uom_greige": 1,
    #             "product_uom": 1,
    #             "lab_id": self.labdip_id.id,
    #             "so_line_id": self.id,
    #             "so_id": self.order_id.id
    #         }
    #     kartu_proses = kp_obj.create(data)
    #     return kartu_proses



# class KartuProsesInherit(models.Model):

#     _inherit = 'kartu.proses'

    # so_line_id     = fields.Many2one('sale.order.line', string='WO Line')
    # qty_process    = fields.Float('Qty Process')
    # warna_id       = fields.Many2one(related='sodet_id.color', string='Warna', store=True)
    # fabric_id      = fields.Char(string='Fabric Code',related='sodet_id.order_id.fabric_code',store=True)
    # hanger_code    = fields.Many2one(related='sodet_id.order_id.hanger_code',string='Kode Hanger', store=True)
    # # qty_kg         = fields.Float(string='Kg',related='sodet_id.qty_weight',store=True) di pindah ke tj_mkt_order
    # # qty_mtr        = fields.Float(string='Mtr',related='sodet_id.qty_meter',store=True) di pindah ke tj_mkt_order
    # # qty_yds        = fields.Float(string='Yds',related='sodet_id.qty_length',store=True) di pindah ke tj_mkt_order
    # article_name   = fields.Char(String="Article Name",related='sodet_id.order_id.article_name',store=True)
    # color_way      = fields.Many2one(related='warna_id', string='Color Way', store=True)
    # fabric_base    = fields.Char(String="Fabric Base",related='sodet_id.order_id.fabric_base',store=True)
    # qty_per_pieces = fields.Float(String="Qty per Pieces",related='sodet_id.qty_length',store=True)


#     type_kp     = fields.Selection(string="Type KP", selection=[
#                     ('d','Dyeing'),
#                     ('p','Printing'),
#                     ],required=False)
#     category_id = fields.Many2one('sale.contract.category', related="so_line_id.order_id.contract_id.category_id", string='Type KP',store=True)
#     partner_id  = fields.Many2one('res.partner', string='Partner',related='so_line_id.order_id.partner_id', store=True)


#     @api.onchange('so_id')
#     def onchange_so_id(self):
#         return {'domain': {'so_line_id': [('order_id','=', self.so_id.id),('qty_remaining','>',0)]}}

#     @api.multi
#     def create_kp_from_wo_line(self):
#         action = self.env.ref('tj_mkt_order.action_kartu_proses_list').read()[0]
#         action['views'] = [(self.env.ref('tj_mkt_order.tj_kartu_proses_form').id, 'form')]
#         action['res_id'] = self.id

#         return action


#     def _onchange_so_line(self, values):
#         if 'so_line_id' in values.keys():
#             if values['so_line_id']:
#                 so_line = self.env['sale.order.line'].browse(values['so_line_id'])
#                 so_line.write({'kp_existed' : True})

#     @api.model
#     def create(self, values):
#         self._onchange_so_line(values)
#         res = super(KartuProsesInherit, self).create(values)
#         return res

#     @api.multi
#     def write(self, values):
#         for kp in self:
#             old_so_line = self.so_line_id
#             if 'so_line_id' in values.keys():
#                 if len(old_so_line.kp_ids) == 1 and old_so_line.id != values['so_line_id']:
#                     old_so_line.write({'kp_existed' : False})

#             kp._onchange_so_line(values)

#         res = super(KartuProsesInherit, self).write(values)
#         if 'qty_process' in values.keys():
#             self.so_line_id.getQtySummary()
#         return res


