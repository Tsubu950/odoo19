from odoo import models, fields

class SmartenOccupancySnapshot(models.Model):
    _name = 'smarten.occupancy.snapshot'
    _description = 'Real‑Time Occupancy Snapshot'
    _order = 'timestamp desc'

    timestamp = fields.Datetime(default=fields.Datetime.now)
    total_occupancy = fields.Integer()
    camera_site = fields.Char()
    details = fields.Text()