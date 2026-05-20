from odoo import models, fields

class SmartenBlockedLog(models.Model):
    _name = 'smarten.blocked.log'
    _description = 'Blocked Person Attempts'
    _order = 'entry_time desc'

    employee_id = fields.Many2one('hr.employee', string='Blocked Person', required=True, domain=[('is_blocked','=',True)])
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    photo = fields.Binary(string='Snapshot', attachment=True)
    alert_sent = fields.Boolean(default=False)
    timestamp = fields.Datetime(default=fields.Datetime.now)