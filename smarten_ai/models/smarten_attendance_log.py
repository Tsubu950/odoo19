from odoo import models, fields, api
from datetime import timedelta

class SmartenAttendanceLog(models.Model):
    _name = 'smarten.attendance.log'
    _description = 'Attendance Log (with AI metadata)'
    _order = 'entry_time desc'
    _rec_name = 'person_id'

    person_id = fields.Many2one('hr.employee', string='Person', required=True, ondelete='cascade')
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float(compute='_compute_duration', store=True)
    person_type = fields.Selection(related='person_id.role', string='Role', store=True)
    liveness_score = fields.Float(string='Liveness Score')
    reid_embedding = fields.Text(string='ReID Embedding')
    photo = fields.Binary(string='Snapshot', attachment=True)
    is_anomaly = fields.Boolean(string='Anomaly')
    shift_id = fields.Many2one('smarten.shift.schedule', string='Shift')
    timestamp = fields.Datetime(default=fields.Datetime.now)

    @api.depends('entry_time', 'exit_time')
    def _compute_duration(self):
        for rec in self:
            if rec.entry_time and rec.exit_time:
                diff = rec.exit_time - rec.entry_time
                rec.duration = diff.total_seconds() / 3600.0
            else:
                rec.duration = 0.0

    def auto_close_stale_sessions(self):
        hours = int(self.env['ir.config_parameter'].sudo().get_param('smarten_ai.auto_close_hours', 12))
        cutoff = fields.Datetime.now() - timedelta(hours=hours)
        stale = self.search([('exit_time', '=', False), ('entry_time', '<', cutoff)])
        for rec in stale:
            rec.write({'exit_time': cutoff, 'duration': (cutoff - rec.entry_time).total_seconds()/3600.0, 'is_anomaly': True})

    def generate_weekly_report(self):
        from datetime import datetime, timedelta
        one_week_ago = datetime.now() - timedelta(days=7)
        logs = self.search([('entry_time', '>=', one_week_ago)])
        # Generate PDF using QWeb
        report = self.env['ir.actions.report']._get_report_from_name('smarten_ai.weekly_attendance_report')
        pdf = report._render_qweb_pdf(logs.ids)[0]
        # Email to managers (simplified)
        template = self.env.ref('smarten_ai.mail_template_weekly_report')
        template.send_mail(logs[0].id, force_send=True)
        return True