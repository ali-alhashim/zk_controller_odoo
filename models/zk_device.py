from odoo import models, fields, api

class ZkDevice(models.Model):
    _name        = 'zk.device'
    _description = 'ZK Devices List'
    model        = fields.Char(string='Model')
    serial_number= fields.Char(string='Serial Number')
    area_name    = fields.Char(string='Area Name')
    ip_address   = fields.Char(string='IP Address')
    is_online    = fields.Boolean(string='Is Online', default=False)
    # One2many field to reference all related attendances (not required but useful for reverse lookup)
    attendance_ids = fields.One2many('hr.attendance', 'zk_device_id', string='Attendances')
