from odoo import models, fields

class GymAnalytics(models.Model):
    _name = 'gym.analytics'
    _description = 'Daily Analytics Snapshot'
    _rec_name = 'date'

    date = fields.Date(string='Date', default=fields.Date.today, required=True, index=True)
    male_count = fields.Integer(string='Male Count')
    female_count = fields.Integer(string='Female Count')
    age_distribution = fields.Text(string='Age Distribution', help='JSON format')
    peak_hour = fields.Integer(string='Peak Hour')
    total_visits = fields.Integer(string='Total Visits')

    _sql_constraints = [
        ('date_unique', 'unique(date)', 'An analytics record already exists for this date.')
    ]