from odoo import models, fields

class SmartenVipLog(models.Model):
    _name = 'smarten.vip.log'
    _description = 'VIP Entry Log'
    _order = 'entry_time desc'

    employee_id = fields.Many2one('hr.employee', string='VIP Person', required=True, domain=[('is_vip','=',True)])
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    photo = fields.Binary(string='Snapshot', attachment=True)
    gender = fields.Char()
    age_range = fields.Char()
    timestamp = fields.Datetime(default=fields.Datetime.now)