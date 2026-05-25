from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Role classification for attendance filtering (owners, board members, staff)
    role = fields.Selection([
        ('owner', 'Owner'),
        ('board_member', 'Board Member'),
        ('staff', 'Staff')
    ], string='Role', default='staff', help='Used for attendance reports and filtering.')

    is_vip = fields.Boolean(string='VIP', default=False)
    is_blocked = fields.Boolean(string='Blocked', default=False)
    blocked_reason = fields.Text(string='Blocked Reason')
    face_image = fields.Binary(string='Face Photo (for AI)', attachment=True)
    ai_face_encoding = fields.Text(string='Face Encoding')
    firebase_token = fields.Char(string='Firebase Token')
    telegram_chat_id = fields.Char(string='Telegram Chat ID')
    shift_ids = fields.One2many('smarten.shift.schedule', 'employee_id', string='Shifts')