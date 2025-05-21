# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomModuleScan(models.Model):
    _name = 'custom.module.scan'
    _description = 'Scan Modul Menu'

    employee_barcode = fields.Char('Badge ID')
    kartu_proses_barcode = fields.Char('Kartu Proses ID')

    name = fields.Char('name')
    proses_ids = fields.Many2many('kartu.proses.flow.proses', string='Flow Proses')
    # field_name_id = fields.Many2one('hr.employee', string='barcode')

    @api.onchange('employee_barcode', 'kartu_proses_barcode')
    def _check_barcode_data(self):
        employee = self.env['hr.employee'].search([('barcode', '=', self.employee_barcode)], limit=1)
        
        if employee and employee.is_op_dyeing:
            kartu_proses = self.env['kartu.proses'].search([('name', '=', self.kartu_proses_barcode)], limit=1)
            if kartu_proses:
                raise UserError("Data tersedia: Barcode employee dan kartu proses ditemukan.")
            else:
                raise UserError("Data tidak ditemukan: Kartu Proses tidak cocok.")
        elif employee:
            raise UserError("Employee ditemukan tetapi status operasi tidak sesuai.")
        elif self.employee_barcode and not employee:
            raise UserError("Data tidak ditemukan: Barcode Employee tidak ada.")
        elif self.kartu_proses_barcode:
            raise UserError("Data tidak ditemukan: Barcode Kartu Proses tidak ada.")

    

