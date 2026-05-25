from odoo import models, fields, api
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class SmartenAttendanceProcessor(models.AbstractModel):
    _name = 'smarten.attendance.processor'
    _description = 'Process raw attendance logs into final records'

    @api.model
    def process_daily_attendance(self):
        """Group raw IN/OUT logs by employee and date, calculate durations."""
        logs = self.env['smarten.attendance.log'].search(
            [('person_id', '!=', False)], order='entry_time'
        )
        # Group by employee and date
        sessions = {}
        for log in logs:
            if not log.entry_time:
                continue
            date = log.entry_time.date()
            employee = log.person_id
            key = (employee.id, date)
            if key not in sessions:
                sessions[key] = {'in': None, 'out': None, 'logs': []}
            if log.direction == 'IN':
                sessions[key]['in'] = log.entry_time
                sessions[key]['logs'].append(log)
            elif log.direction == 'OUT':
                sessions[key]['out'] = log.exit_time or log.entry_time
                sessions[key]['logs'].append(log)

        for (emp_id, date), session in sessions.items():
            if session['in'] and session['out']:
                duration = (session['out'] - session['in']).total_seconds() / 3600.0
                # Create or update native hr.attendance record
                attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', emp_id),
                    ('check_in', '>=', fields.Datetime.to_datetime(f"{date} 00:00:00")),
                    ('check_in', '<=', fields.Datetime.to_datetime(f"{date} 23:59:59")),
                ], limit=1)
                if attendance:
                    attendance.write({'check_out': session['out']})
                else:
                    self.env['hr.attendance'].create({
                        'employee_id': emp_id,
                        'check_in': session['in'],
                        'check_out': session['out'],
                    })
            elif session['in'] and not session['out']:
                # Missing OUT – auto‑close after a default shift length (e.g., 9h)
                auto_out = session['in'] + timedelta(hours=9)
                self.env['hr.attendance'].create({
                    'employee_id': emp_id,
                    'check_in': session['in'],
                    'check_out': auto_out,
                })
        _logger.info("Daily attendance processing completed")