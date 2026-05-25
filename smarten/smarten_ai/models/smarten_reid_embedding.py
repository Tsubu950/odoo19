from odoo import models, fields

class SmartenReidEmbedding(models.Model):
    _name = 'smarten.reid.embedding'
    _description = 'Re‑Identification Embeddings'
    _rec_name = 'person_name'

    person_name = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    embedding = fields.Text(required=True)
    camera_source = fields.Char()
    first_seen = fields.Datetime(default=fields.Datetime.now)
    last_seen = fields.Datetime()
    track_id = fields.Char()