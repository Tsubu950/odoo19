from odoo import models, api, fields
from datetime import datetime, timedelta
import base64

class SmartenWeeklyReport(models.AbstractModel):
    _name = 'report.smarten_ai.weekly_attendance_report'
    _description = 'Weekly Attendance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['smarten.attendance.log'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'smarten.attendance.log',
            'docs': docs,
            'data': data,
        }

class SmartenMonthlyReport(models.AbstractModel):
    _name = 'report.smarten_ai.monthly_attendance_report'
    _description = 'Monthly Attendance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['smarten.attendance.log'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'smarten.attendance.log',
            'docs': docs,
            'data': data,
        }