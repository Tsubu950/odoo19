from odoo import models, fields

class GymCoveredLog(models.Model):
    _name = 'gym.covered.log'
    _description = 'Face Covered / Occluded Events'
    _order = 'timestamp desc'
    _rec_name = 'tracking_id'

    tracking_id = fields.Char(string='Tracking ID', index=True)
    image = fields.Binary(string='Full Body Image', attachment=True)
    video_clip = fields.Char(string='Video Clip Path', help='Local path to saved clip')
    gender = fields.Char(string='Estimated Gender')
    age_range = fields.Char(string='Estimated Age Range')
    camera_source = fields.Selection([
        ('entry', 'Entry Camera'),
        ('exit', 'Exit Camera')
    ], string='Camera Source')
    reason = fields.Char(string='Reason', default='face_not_visible')
    timestamp = fields.Datetime(string='Event Time', default=fields.Datetime.now, required=True)
    is_suspicious = fields.Boolean(string='Suspicious Repeated', default=False)