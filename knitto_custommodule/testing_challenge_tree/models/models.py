# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TestingChallengeTree(models.Model):
    _name = 'testing.challenge.tree'
    _description = 'Model Challenge Tree'

    name = fields.Char('Nama')
    kebutuhan_uan = fields.Integer('Kebutuhan Uang')
    