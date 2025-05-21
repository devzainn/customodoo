from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, Warning


class SaleContractStockGreige(models.Model):

    _name = 'sale.order.stock.gudang.jadi'

    sale_order_id = fields.Many2one('sale.order',ondelete="cascade")
    order_line_id = fields.Many2one('sale.order.line',ondelete="cascade")
    product_id = fields.Many2one('product.product', related='order_line_id.product_id', string='Product')

    product_available = fields.Float(string='Product Available')
    product_quant = fields.Float(string='Product Quant')


class SaleOrderInherit(models.Model):

    _inherit = 'sale.order'


    stock_gudang_jadi_line_ids  = fields.One2many('sale.order.stock.gudang.jadi','sale_order_id',string='Daftar Stock Gudang Jadi')


    def get_location_data(self):

        setLocation = set()
        warehouseContractPool = self.env['stock.warehouse'].search([('is_mkt_order_sales','=',True)])
        for rec in warehouseContractPool:
            for recData in rec.lot_stock_id.location_ids:
                setLocation.add(recData.id)


        return setLocation

    def generate_stock_gudang_jadi_ids(self,paramLine):

        stock_gjadi_ids = []
        kondisi = True
        
        locationIds = self.get_location_data()        
        if(len(locationIds)==0):
            kondisi = False
        
        locationIds = str(tuple(locationIds)).replace(',)',')')

        for recLine in paramLine:

            query = ""
            if(kondisi==True):
                query = """
                        SELECT 
                            SUM(q.qty) as qty
                        FROM
                            stock_quant q
                        WHERE
                            location_id in %s
                            AND product_id = %s
                    """%(locationIds, recLine.product_id.id)
            else:
                query = """
                        SELECT 
                            SUM(q.qty) as qty
                        FROM
                            stock_quant q
                        WHERE
                            product_id = %s
                    """%(recLine.product_id.id)
            
            
            self._cr.execute(query)
            result = self._cr.dictfetchall()
            available_qty = result[0]['qty'] or 0
           

            stock_gjadi_ids.append([0,0,{
                'sale_order_id':recLine.order_id.id,
                'order_line_id':recLine.id,
                'product_id':recLine.product_id.id,
                'product_available':available_qty,
                'product_quant':available_qty,
            }])

        return stock_gjadi_ids




    @api.model
    def create(self, vals):

        res = super(SaleOrderInherit, self).create(vals)
        
        for rec in res:

            stock_gjadi_ids = self.generate_stock_gudang_jadi_ids(rec.order_line)
            if(len(stock_gjadi_ids)>0):
                rec.stock_gudang_jadi_line_ids = stock_gjadi_ids

        return res


    @api.multi
    def write(self, vals):

        result = super(SaleOrderInherit, self).write(vals)

        if('order_line' in vals):           
            
            for rec in self.search([('id','=',self.id)]):            

                for recStock in rec.stock_gudang_jadi_line_ids:
                    recStock.unlink()


                stock_gjadi_ids = self.generate_stock_gudang_jadi_ids(rec.order_line)
                if(len(stock_gjadi_ids)>0):
                    rec.stock_gudang_jadi_line_ids = stock_gjadi_ids
            

        return result
