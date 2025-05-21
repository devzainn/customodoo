from odoo import models, fields, api
import json

class PlanningGlobal(models.Model):
    _name = 'planning.global'

    name       = fields.Char(string='No WO')
    process_id = fields.Many2one('master.proses.wip', string='Process Wip')
    process    = fields.Char(string='Process')
    quantity   = fields.Float(string='Quantity')
    date       = fields.Datetime(string='Date')
    state      = fields.Boolean(string='State')
    wo_id      = fields.Many2one('sale.order', string='WO ID')
    user_id    = fields.Many2one('hr.employee', string='User')
    no_urut    = fields.Integer(string='No Urut',)
    is_selesai = fields.Boolean(string='Is Selesai', default=False)
    date_plan  = fields.Date(string='Date Plan')


    @api.model
    def check_connection(self):
        return True

    @api.model
    def get_data_planning_global(self, date_start, date_end):
        print(date_start)
        print(date_end)
        master_process = []
        data_process   = []
        wo             = []
        kapasitas_kg   = {}
        kategori_wip   = []

        query_master_process      = """ select name from master_proses_wip ORDER BY urutan"""
        # query_data_process        = """ SELECT planning_global.id, planning_global.process as name, planning_global.name as wo_id, planning_global.quantity as qty, planning_global.date, planning_global.state FROM planning_global JOIN master_proses_wip ON master_proses_wip.id = planning_global.process_id where planning_global.is_selesai = false limit 20"""
        query_data_process        = """ SELECT planning_global.id, planning_global.process as name, planning_global.name as wo_id, planning_global.quantity as qty, planning_global.date, planning_global.state FROM planning_global JOIN master_proses_wip ON master_proses_wip.id = planning_global.process_id JOIN sale_order so ON so.id = planning_global.wo_id where planning_global.is_selesai = false and so.wo_date BETWEEN '%s' AND '%s'""" % (date_start, date_end)
        # query_wo                  = """ select name from planning_global where is_selesai = false group by name"""
        query_wo                  = """ SELECT planning_global.name FROM planning_global JOIN sale_order so ON so.id = planning_global.wo_id where planning_global.is_selesai = false and so.wo_date BETWEEN '%s' AND '%s' group by planning_global.name, so.wo_date""" % (date_start, date_end)
        query_kapasitas_mesin_kg  = """ SELECT name,kapasitas_kg FROM master_proses_wip ORDER BY urutan """
        query_kategori_proses_wip = """ SELECT b.id as id_kategori, b.name, COUNT(*) as total_proses FROM master_proses_wip as a LEFT JOIN kategori_master_proses_wip as b ON b.id = a.kategori GROUP BY b.name, b.id ORDER BY b.no_urut"""

        self._cr.execute(query_master_process)
        fetch_master_process = self._cr.dictfetchall()
        for rec in fetch_master_process:
            master_process.append(rec['name'])

        self._cr.execute(query_data_process)    
        fetch_data_process = self._cr.dictfetchall()
        for b in fetch_data_process:
            data_process.append(b)
        
        self._cr.execute(query_wo)
        fetch_wo = self._cr.dictfetchall()
        for c in fetch_wo:
            wo.append(c['name'])
        
        self._cr.execute(query_kapasitas_mesin_kg)
        for m in self._cr.dictfetchall():
            kapasitas_kg[m['name']] = m['kapasitas_kg']

        self._cr.execute(query_kategori_proses_wip)
        for k in self._cr.dictfetchall():
            proses = self.env['master.proses.wip'].search([('kategori','=',k['id_kategori'])], order='urutan asc').mapped('name')
            kategori_wip.append({'kategori' : k['name'], 'total' : k['total_proses'], 'proses' : proses})

        data = {
            "master"       : master_process,
            "process"      : data_process,
            "wo"           : wo,
            "kapasitas_kg" : kapasitas_kg,
            "kategori_wip" : kategori_wip,
        }
        print("==============planning global===========")
        return data

    @api.model
    def update_planning_global(self, id, state):
        print '==========update_planning_global================='
        print id
        print state
        planningGlobalObj = self.env['planning.global']
        date_now = fields.Date.today()
        if state:
            query1 = """UPDATE planning_global set state = true, date = '%s' where id = %s """ % (date_now, id)
            self._cr.execute(query1)
        else:
            query1 = """UPDATE planning_global set state = false, date = null where id = %s """ % (id)
            self._cr.execute(query1)

    @api.model
    def action_selesai(self, no_wo):
        query = """UPDATE planning_global set is_selesai = true where name= '%s';
                   UPDATE sale_order set is_selesai = true where name= '%s'; """ % (no_wo, no_wo)
        self._cr.execute(query)
