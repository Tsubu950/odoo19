from odoo import models, fields, api

class OmniUnknownLog(models.Model):
    _name = 'omni.unknown.log'
    _description = 'Unknown Persons (Face Visible)'
    _order = 'entry_time desc'
    _rec_name = 'unknown_id'

    unknown_id = fields.Char(string='Unique ID', required=True, index=True)
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float(compute='_compute_duration', store=True)
    gender = fields.Char()
    age_range = fields.Char()
    photo = fields.Binary(string='Face Snapshot', attachment=True)

    @api.depends('entry_time','exit_time')
    def _compute_duration(self):
        for rec in self:
            if rec.entry_time and rec.exit_time:
                diff = rec.exit_time - rec.entry_time
                rec.duration = diff.total_seconds() / 3600.0
            else:
                rec.duration = 0.0