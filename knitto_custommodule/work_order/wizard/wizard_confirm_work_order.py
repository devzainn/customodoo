from odoo import models, fields, api,_
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class WizardConfirmWorkOrder(models.TransientModel):

    _name = 'wizard.cofirm.work.order'
    _description = 'Confirm Work Order'


    @api.model
    def proccess_confirm(self, ids,context):

        if(ids):

            poolSaleOrder = self.env['sale.order'].search([('id','in',context['active_ids'])])
            for rec in poolSaleOrder:
                
                if rec.hanger_code.mlot_id:
                    if rec.hanger_code.is_order_pertama == True and rec.hanger_code.mlot_id.state == 'approve_rnd':
                        raise ValidationError(_("Silahkan klik button check terlebih dahulu pada work order dengan nomor : "+ rec.name + " "))

                if rec.is_mlot == False and rec.notulen == False:
                    raise ValidationError(_("Silahkan klik button notulen check terlebih dahulu pada work order dengan nomor : "+ rec.name + " "))




                if(rec.state=='confirm_wo'):
                    raise ValidationError(_("Work / Sale order dengan nomor : "+ rec.name + " sudah berstatus confirm. Anda tidak bisa melakukan konfirmasi ulang"))



                # ------- BEGIN action_assign_manager 
                
                if rec.hanger_code.mlot_id:
                    if rec.hanger_code.is_order_pertama == True and rec.hanger_code.mlot_id.state == 'approve_rnd':
                        raise ValidationError(_("Work / Sale order dengan nomor : " + rec.name + " belum dilakukan tahap cek. Silahkan Klik Button Check terlebih dahulu"))                        
                if rec.is_mlot == False and rec.notulen == False:
                    raise ValidationError(_("Work / Sale order dengan nomor : " + rec.name + " belum dilakukan tahap notulen. Silahkan Klik tombol Notulen terlebih dahulu"))
                    
                
                rec.action_confirm()

                seq_id = self.env['ir.sequence']

                if context.get('is_work_order'):

                    if rec.type == 'dyeing' :
                        rec.name = seq_id.next_by_code('wo.dyeing')
                    elif rec.type == 'printing':
                        rec.name = seq_id.next_by_code('wo.printing')
                    
                    # no = 0
                    # for line in rec.order_line:
                        # monthDict = {"01" : "A",
                        #         "02" : "B",
                        #         "03" : "C",
                        #         "04" : "D",
                        #         "05" : "E",
                        #         "06" : "F",
                        #         "07" : "G",
                        #         "08" : "H",
                        #         "09" : "I",
                        #         "10" : "J",
                        #         "11" : "K",
                        #         "12" : "L"}
                        # bulanCreateKp = monthDict.get(datetime.now().strftime("%m"))
                        # bulanWo  = wo_id.name.split('/')[2]
                        # noUrutWo = wo_id.name.split('/')[3]
                        # line.batch = code + bulanCreateKp + str(no) + bulanWo + noUrutWo
                        # no += 1
                        # line.batch = rec.name.split('/')[3] +  "-" +seq_id.next_by_code('no.batch')
                    
                    rec.create_planning_global()
                    if rec.is_mlot == False:
                        rec.hanger_code.write({'is_order_pertama':True})

                # ------- END action_assign_manager 



                # print " ===== ", rec.name
                
                # print " >>>>> ", rec.name
                # raise UserError('555555555555555555555555555')

                stockPickingCheck = self.env['stock.picking'].search([('sale_id','=',rec.id)])
                for res in stockPickingCheck:
                    originWo = ' (' +  rec.origin + ')' if rec.origin else ''
                    res.origin = rec.name + originWo
                    res.picking_type_id = 178
                    
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
                        res.action_assign()

                # rec.state         = 'confirm_wo'
                # rec.states_greige = 'approve'