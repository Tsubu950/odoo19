from odoo import models, fields, api
from datetime import timedelta

class SmartenRawLog(models.Model):
    _name = 'smarten.raw.log'
    _description = 'Live Raw Detection Feed'
    _order = 'create_date desc'

    track_id = fields.Integer(string='Track ID', required=True, index=True)
    camera_id = fields.Char(string='Camera', default='unknown')
    snapshot = fields.Binary(string='Snapshot', attachment=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    bbox = fields.Char(string='Bounding Box')  # "x1,y1,x2,y2"
    create_date = fields.Datetime(string='Timestamp', readonly=True, index=True)

    def action_cleanup_raw_logs(self):
        """Delete all records older than 1 day (called by cron)."""
        yesterday = fields.Datetime.now() - timedelta(days=1)
        old_records = self.search([('create_date', '<', yesterday)])
        count = len(old_records)
        old_records.unlink()
        return count  # for logging