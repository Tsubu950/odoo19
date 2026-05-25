from odoo import models, fields, api

class SmartenCoveredLog(models.Model):
    _name = 'smarten.covered.log'
    _description = 'Covered / Occluded Faces'
    _order = 'entry_time desc'

    tracking_id = fields.Char(string='Tracking ID', required=True, index=True)
    direction = fields.Selection([('IN','IN'),('OUT','OUT')], required=True)
    camera_source = fields.Selection([('entry','Entry'),('exit','Exit')])
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float(compute='_compute_duration', store=True)
    photo = fields.Binary(string='Full Body Image', attachment=True)
    video_clip = fields.Char(string='Video Clip Path')
    reid_embedding = fields.Text()
    timestamp = fields.Datetime(default=fields.Datetime.now)

    @api.depends('entry_time', 'exit_time')
    def _compute_duration(self):
        for rec in self:
            if rec.entry_time and rec.exit_time:
                diff = rec.exit_time - rec.entry_time
                rec.duration = diff.total_seconds() / 3600.0
            else:
                rec.duration = 0.0