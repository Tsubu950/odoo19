{
    'name': 'Omni AI Monitoring',
    'version': '1.0',
    'category': 'Human Resources/Attendances',
    'summary': 'AI-powered attendance & security monitoring',
    'description': """
        Professional attendance system with:
        - Standard attendance for staff/owners using hr.attendance
        - Separate logs for VIP, blocked, unknown, covered faces
        - Graph/kanban views and real‑time alerts
    """,
    'author': 'Your Company',
    'depends': ['base', 'mail', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_employee_views.xml',
        'views/omni_vip_views.xml',
        'views/omni_blocked_views.xml',
        'views/omni_unknown_views.xml',
        'views/omni_covered_views.xml',
        'views/menu_views.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}