# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class zk_controller(models.Model):
#     _name = 'zk_controller.zk_controller'
#     _description = 'zk_controller.zk_controller'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

