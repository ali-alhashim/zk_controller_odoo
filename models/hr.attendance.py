# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    in_mode = fields.Selection(string="Mode",
                               selection=[('kiosk', "Kiosk"),
                                          ('systray', "Systray"),
                                          ('zk-device','ZK-Device'),
                                          ('manual', "Manual")],
                               readonly=True,
                               default='manual')




