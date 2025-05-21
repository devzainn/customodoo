from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

class WnPreferenceMaster(models.Model):
    _name = 'wn.preference.master'
    _description = 'Pereference Master Table'

    code        = fields.Char('Pref Code', default="#01")
    name        = fields.Char('Pref Name', )