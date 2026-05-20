from odoo import models, fields, api

class SmartenShiftSchedule(models.Model):
    _name = 'smarten.shift.schedule'
    _description = 'Shift Schedule'
    _order = 'shift_date desc, start_time'

    employee_id = fields.Many2one('hr.employee', required=True)
    shift_date = fields.Date(required=True)
    start_time = fields.Datetime(required=True)
    end_time = fields.Datetime(required=True)
    expected_hours = fields.Float(compute='_compute_expected', store=True)
    attendance_id = fields.Many2one('smarten.attendance.log')
    actual_duration = fields.Float()
    status = fields.Selection([
        ('pending','Pending'), ('on_time','On Time'), ('late','Late'),
        ('absent','Absent'), ('early_leave','Early Leave')
    ], compute='_compute_status', store=True)

    @api.depends('start_time', 'end_time')
    def _compute_expected(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                rec.expected_hours = (rec.end_time - rec.start_time).total_seconds() / 3600.0
            else:
                rec.expected_hours = 0

    @api.depends('attendance_id', 'actual_duration', 'expected_hours', 'start_time')
    def _compute_status(self):
        for rec in self:
            if not rec.attendance_id:
                rec.status = 'absent'
            else:
                late_threshold = 15 * 60
                if rec.attendance_id.entry_time and (rec.attendance_id.entry_time - rec.start_time).total_seconds() > late_threshold:
                    rec.status = 'late'
                elif rec.actual_duration < rec.expected_hours * 0.9:
                    rec.status = 'early_leave'
                else:
                    rec.status = 'on_time'