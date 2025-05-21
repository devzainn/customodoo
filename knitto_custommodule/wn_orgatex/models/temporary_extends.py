from __future__ import division
from types import NoneType
from odoo import fields, models, api, _
from odoo.http import request
from odoo.exceptions import Warning,ValidationError,UserError
import json
import time
import datetime
import logging
import re
import numpy as np
_logger = logging.getLogger(__name__)
import mysql.connector

# # SQL_URL = "idola.3dimensi.net"
# SQL_URL = "127.0.0.1"
# # SQL_URL = "isa.wibicon.com"
# SQL_USER = 'root'
# SQL_PASS = ''
# SQL_DEBE = 'db_testing'

class TemporaryExtends(models.Model):
    _name = 'temporary.extends'
    _description = 'Temporary Extends Table'
    _rec_name = 'data_id'

    data_id = fields.Many2one('wn.orgatex', string='data')
    qty_receipt = fields.Float(string="Quantity Receipt", digits=(16, 5))
    qty_actual = fields.Float(string="Quantity Actual", digits=(16, 5))
    batch_ref = fields.Char(
        string="Batch Reference", 
        related='data_id.batch_ref', 
        store=True
    )
    proses_id = fields.Many2one(
        string="Process", 
        related='data_id.proses_id', 
        store=True
    )

    # conn = None
    # data = None
    # child = None
    # by_date = None
    # by_barcode = None
    # data_barcode = None
    
    # @api.model
    # def get_inspect(self):
    #     start = time.time()
    #     self.connect_mysql()
    #     uid = request.session.uid
    #     cr = self.env.cr

    # def connect_mysql(self):
    #     self.conn = mysql.connector.connect(user=SQL_USER,
    #                                         password=SQL_PASS,
    #                                         host=SQL_URL,
    #                                         database=SQL_DEBE)

    # def disconnect_mysql(self):
    #     self.conn.close()


    def write(self, vals):
        """
        Override method write untuk mengupdate data di wn.orgatex
        ketika qty_actual diubah.
        """
        res = super(TemporaryExtends, self).write(vals)

        if 'qty_actual' in vals:
            for record in self:
                if record.data_id: 
                    record.data_id.sudo().write({
                        'qty_receipt': record.qty_actual 
                    })
                    _logger.info(
                        "Updated wn.orgatex record (ID: %s) with qty_receipt: %s",
                        record.data_id.id, record.qty_actual
                    )

                    picking = record.data_id.source_id.picking_id
                    if picking:
                        for move in picking.move_lines:
                            if (move.product_id.name == record.data_id.product_name and move.tahapan == record.data_id.no_program ):
                                qty_actual_rounded = round(record.qty_actual, 6) 
                                move.sudo().write({
                                    'product_uom_qty': qty_actual_rounded
                                })
                                _logger.info(
                                    "Updated stock.move (ID: %s) in picking (ID: %s) with product_uom_qty: %.4f",
                                    move.id, picking.id, qty_actual_rounded
                                )
                                
                        if picking.state != 'draft':
                            picking.sudo().write({'state': 'draft'})
                            _logger.info(
                                "Updated stock.picking (ID: %s) state to 'draft'",
                                picking.id
                            )
        return res