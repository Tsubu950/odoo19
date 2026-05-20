from odoo import models, fields, api

class OmniVipLog(models.Model):
    _name = 'omni.vip.log'
    _description = 'VIP Attendance Log'
    _order = 'entry_time desc'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='VIP Person', required=True, domain=[('is_vip','=',True)])
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float(compute='_compute_duration', store=True)
    photo = fields.Binary(string='Snapshot', attachment=True)
    gender = fields.Char()
    age_range = fields.Char()

    @api.depends('entry_time','exit_time')
    def _compute_duration(self):
        for rec in self:
            if rec.entry_time and rec.exit_time:
                diff = rec.exit_time - rec.entry_time
                rec.duration = diff.total_seconds() / 3600.0
            else:
                rec.duration = 0.0