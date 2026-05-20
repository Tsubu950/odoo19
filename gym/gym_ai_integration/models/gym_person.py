from odoo import models, fields, api

class GymPerson(models.Model):
    _name = 'gym.person'
    _description = 'Members & Staff'
    _inherit = ['image.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Full Name', required=True, index=True)
    role = fields.Selection([
        ('member', 'Member'),
        ('staff', 'Staff')
    ], string='Role', default='member', required=True)
    rfid_tag = fields.Char(string='RFID UID', index=True)
    image = fields.Image(string='Photo', max_width=1920, max_height=1920)
    active = fields.Boolean(string='Active', default=True)
    face_encoding = fields.Text(string='Face Embedding Vector', help='Reserved for future use')

    # One2many relations
    attendance_ids = fields.One2many('gym.attendance.log', 'person_id', string='Attendance Logs')
    total_visits = fields.Integer(compute='_compute_total_visits', string='Total Visits', store=True)

    @api.depends('attendance_ids')
    def _compute_total_visits(self):
        for rec in self:
            rec.total_visits = len(rec.attendance_ids.filtered(lambda a: a.direction == 'IN'))