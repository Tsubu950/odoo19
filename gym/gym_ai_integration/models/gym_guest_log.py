from odoo import models, fields

class GymGuestLog(models.Model):
    _name = 'gym.guest.log'
    _description = 'Unknown Guest Entries'
    _order = 'timestamp desc'
    _rec_name = 'guest_id'

    guest_id = fields.Char(string='Guest ID', required=True, index=True)
    image = fields.Binary(string='Snapshot', attachment=True)
    gender = fields.Char(string='Gender')
    age_range = fields.Char(string='Age Range')
    camera_source = fields.Selection([
        ('entry', 'Entry Camera'),
        ('exit', 'Exit Camera')
    ], string='Camera Source')
    timestamp = fields.Datetime(string='Detected At', default=fields.Datetime.now, required=True)
    is_resolved = fields.Boolean(string='Converted to Member', default=False)