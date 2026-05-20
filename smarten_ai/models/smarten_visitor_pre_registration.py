from odoo import models, fields, api

class SmartenVisitorPreRegistration(models.Model):
    _name = 'smarten.visitor.pre_registration'
    _description = 'Visitor Pre‑Registration'
    _rec_name = 'visitor_name'

    visitor_name = fields.Char(required=True)
    email = fields.Char()
    phone = fields.Char()
    visit_date = fields.Date(required=True)
    host_id = fields.Many2one('hr.employee', string='Host')
    purpose = fields.Text()
    face_image = fields.Binary(string='Face Photo', attachment=True)
    face_encoding = fields.Text()
    status = fields.Selection([
        ('pending','Pending'), ('approved','Approved'),
        ('checked_in','Checked In'), ('checked_out','Checked Out'), ('expired','Expired')
    ], default='pending')
    token = fields.Char(string='Access Token', readonly=True, copy=False)
    check_in_time = fields.Datetime()
    check_out_time = fields.Datetime()

    @api.model
    def create(self, vals):
        vals['token'] = self.env['ir.sequence'].next_by_code('smarten.visitor.token') or 'VIS'
        return super().create(vals)
    @api.model
    def _get_next_token(self):
        seq = self.env['ir.sequence'].search([('code', '=', 'smarten.visitor.token')], limit=1)
        if not seq:
            seq = self.env['ir.sequence'].create({
                'name': 'Visitor Token',
                'code': 'smarten.visitor.token',
                'padding': 5,
            })
        return seq.next_by_id()