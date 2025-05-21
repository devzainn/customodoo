from odoo import models, fields, api
import json

class PlanningGlobalKp(models.Model):
    _name = 'planning.global.kp'

    name       = fields.Char(string='No WO')
    wo_line_id = fields.Many2one('sale.order.line', string='WO CW')
    batch 	   = fields.Char(string='Batch', related="wo_line_id.batch", store=True,)
    kp_id      = fields.Many2one('kartu.proses', string='No KP')
    process_id = fields.Many2one('master.proses.wip', string='Process Wip')
    process    = fields.Char(related='process_id.name', store=True,)
    quantity   = fields.Float(string='Quantity')
    date       = fields.Date(string='Date')
    state      = fields.Boolean(string='State')
    wo_id      = fields.Many2one('sale.order', string='WO ID')
    user_id    = fields.Many2one('hr.employee', string='User')
    no_urut    = fields.Integer(string='No Urut', related="process_id.urutan", store=True,)

    @api.model
    def get_data_planning_global_batch(self):
        master_process = []
        data_process   = []
        wo             = []

        query_master_process = """ select name from master_proses_wip """
        self._cr.execute(query_master_process)
        fetch_master_process = self._cr.dictfetchall()
        for rec in fetch_master_process:
            master_process.append(rec['name'])
        query_data_process = """ SELECT a.id, a.process as name, a.name as wo_id, a.quantity as qty, a.date, a.state FROM planning_global_batch a JOIN master_proses_wip b ON b.id = a.process_id """
        self._cr.execute(query_data_process)    
        fetch_data_process = self._cr.dictfetchall()
        for b in fetch_data_process:
            data_process.append(b)
        query_wo = """ select name from planning_global_kp group by name """
        self._cr.execute(query_wo)
        fetch_wo = self._cr.dictfetchall()
        for c in fetch_wo:
            wo.append(c['name'])

        data = {
            "master"       : master_process,
            "process" : data_process,
            "wo"           : wo
        }

        print '=============global kp ==========='
        print data
        return data

    @api.model
    def update_planning_global_kp(self, id, state):
        print '==========update_planning_global_kp'
        print id
        print state
        planningGlobalObj = self.env['planning.global.kp']
        date_now = fields.Date.today()
        if state:
            query1 = """UPDATE planning_global_kp set state = true, date= '%s' where id = %s """ % (id, date_now)
            self._cr.execute(query1)
        else:
            query1 = """UPDATE planning_global_kp set state = false, date = null where id = %s """ % (id)
            self._cr.execute(query1)
        return 55

