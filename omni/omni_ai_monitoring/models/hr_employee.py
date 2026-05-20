from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_vip = fields.Boolean(string='VIP', default=False)
    is_blocked = fields.Boolean(string='Blocked', default=False)
    blocked_reason = fields.Text(string='Blocked Reason')
    face_image = fields.Binary(string='Face Photo (for AI)', attachment=True)
    ai_face_encoding = fields.Text(string='Face Encoding')