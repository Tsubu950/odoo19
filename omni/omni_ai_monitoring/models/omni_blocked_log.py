from odoo import models, fields, api

class OmniBlockedLog(models.Model):
    _name = 'omni.blocked.log'
    _description = 'Blocked Person Entry Attempts'
    _order = 'entry_time desc'

    employee_id = fields.Many2one('hr.employee', string='Blocked Person', required=True, domain=[('is_blocked','=',True)])
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float(compute='_compute_duration', store=True)
    photo = fields.Binary(string='Snapshot', attachment=True)
    alert_sent = fields.Boolean(default=False)

    @api.depends('entry_time','exit_time')
    def _compute_duration(self):
        for rec in self:
            if rec.entry_time and rec.exit_time:
                diff = rec.exit_time - rec.entry_time
                rec.duration = diff.total_seconds() / 3600.0
            else:
                rec.duration = 0.0