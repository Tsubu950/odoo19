from odoo import models, fields, api

class GymAttendanceLog(models.Model):
    _name = 'gym.attendance.log'
    _description = 'Entry/Exit Log for Members & Staff'
    _order = 'timestamp desc'
    _rec_name = 'person_id'

    person_id = fields.Many2one('gym.person', string='Person', required=True, ondelete='cascade')
    direction = fields.Selection([
        ('IN', 'IN'),
        ('OUT', 'OUT')
    ], string='Direction', required=True)
    camera_source = fields.Selection([
        ('entry', 'Entry Camera'),
        ('exit', 'Exit Camera')
    ], string='Camera Source')
    person_type = fields.Selection([
        ('member', 'Member'),
        ('staff', 'Staff')
    ], string='Person Type', related='person_id.role', store=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)

    # Duration if both entry and exit exist – computed from pair (optional)
    duration = fields.Float(string='Duration (Hours)', compute='_compute_duration', store=False)

    def _compute_duration(self):
        for rec in self:
            if rec.direction == 'OUT':
                # Find the last IN record for the same person
                last_in = self.search([
                    ('person_id', '=', rec.person_id.id),
                    ('direction', '=', 'IN'),
                    ('timestamp', '<', rec.timestamp)
                ], limit=1, order='timestamp desc')
                if last_in:
                    diff = rec.timestamp - last_in.timestamp
                    rec.duration = diff.total_seconds() / 3600.0
                else:
                    rec.duration = 0.0
            else:
                rec.duration = 0.0