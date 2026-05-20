from odoo import models, fields, api

class SmartenUnifiedLog(models.Model):
    _name = 'smarten.unified.log'
    _description = 'Unified Event Log (SQL View)'
    _auto = False
    _rec_name = 'person_name'

    # Define all fields (id is a plain Integer)
    id = fields.Integer(string='ID', readonly=True)
    person_name = fields.Char()
    category = fields.Selection([
        ('employee', 'Employee'),
        ('vip', 'VIP'),
        ('blocked', 'Blocked'),
        ('unknown', 'Unknown'),
        ('covered', 'Covered')
    ])
    direction = fields.Selection([('IN', 'IN'), ('OUT', 'OUT')])
    camera_source = fields.Char()
    entry_time = fields.Datetime()
    exit_time = fields.Datetime()
    duration = fields.Float()
    gender = fields.Char()
    age_range = fields.Char()
    timestamp = fields.Datetime()

    def init(self):
        # Drop the existing view if it exists (to avoid "cannot change name" errors)
        self.env.cr.execute("DROP VIEW IF EXISTS smarten_unified_log CASCADE")
        sql = """
        CREATE OR REPLACE VIEW smarten_unified_log AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY timestamp DESC) AS id,
            person_name,
            category,
            direction,
            camera_source,
            entry_time,
            exit_time,
            duration,
            gender,
            age_range,
            timestamp
        FROM (
            -- Employee attendance
            SELECT
                'employee'::varchar as category,
                e.name as person_name,
                l.direction,
                l.camera_source,
                l.entry_time,
                l.exit_time,
                l.duration,
                NULL::varchar as gender,
                NULL::varchar as age_range,
                l.timestamp
            FROM smarten_attendance_log l
            JOIN hr_employee e ON l.person_id = e.id

            UNION ALL

            -- VIP logs
            SELECT
                'vip'::varchar,
                e.name,
                l.direction,
                l.camera_source,
                l.entry_time,
                l.exit_time,
                COALESCE(EXTRACT(EPOCH FROM (l.exit_time - l.entry_time))/3600.0, 0.0) as duration,
                l.gender,
                l.age_range,
                l.timestamp
            FROM smarten_vip_log l
            JOIN hr_employee e ON l.employee_id = e.id

            UNION ALL

            -- Blocked logs
            SELECT
                'blocked'::varchar,
                e.name,
                l.direction,
                l.camera_source,
                l.entry_time,
                l.exit_time,
                COALESCE(EXTRACT(EPOCH FROM (l.exit_time - l.entry_time))/3600.0, 0.0),
                NULL,
                NULL,
                l.timestamp
            FROM smarten_blocked_log l
            JOIN hr_employee e ON l.employee_id = e.id

            UNION ALL

            -- Unknown logs
            SELECT
                'unknown'::varchar,
                l.unknown_id,
                l.direction,
                l.camera_source,
                l.entry_time,
                l.exit_time,
                COALESCE(EXTRACT(EPOCH FROM (l.exit_time - l.entry_time))/3600.0, 0.0),
                l.gender,
                l.age_range,
                l.timestamp
            FROM smarten_unknown_log l

            UNION ALL

            -- Covered logs
            SELECT
                'covered'::varchar,
                l.tracking_id,
                l.direction,
                l.camera_source,
                l.entry_time,
                l.exit_time,
                COALESCE(EXTRACT(EPOCH FROM (l.exit_time - l.entry_time))/3600.0, 0.0),
                NULL,
                NULL,
                l.timestamp
            FROM smarten_covered_log l
        ) AS unified
        """
        self.env.cr.execute(sql)