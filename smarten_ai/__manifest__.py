{
    'name': 'Smarten AI',
    'version': '1.0',
    'category': 'Operations/Smarten',
    'summary': 'AI‑powered attendance, security & analytics',
    'description': """
        Enterprise AI monitoring system:
        - Real‑time face recognition (staff, VIP, blocked)
        - Unknown and covered face logging
        - Visitor pre‑registration with face upload
        - Shift scheduling & compliance
        - Cross‑camera re‑identification
        - Liveness detection scoring
        - Real‑time occupancy dashboard
        - Push notifications (Firebase) & Telegram/WhatsApp bot
        - Auto‑generated weekly/monthly PDF reports
        - All edge‑case conditions handled (cooldown, duplicates, missing events)
    """,
    'author': 'Smarten AI',
    'depends': ['base', 'mail', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/notification_templates.xml',
        'data/cron_jobs.xml',
        'views/hr_employee_views.xml',
        'views/smarten_attendance_views.xml',
        'views/smarten_unknown_views.xml',
        'views/smarten_covered_views.xml',
        'views/smarten_vip_views.xml',
        'views/smarten_blocked_views.xml',
        'views/smarten_unified_views.xml',
        'views/smarten_visitor_views.xml',
        'views/smarten_shift_views.xml',
        'views/smarten_occupancy_dashboard.xml',
        'views/smarten_reid_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_views.xml',
        'report/weekly_report_data.xml',
        'report/monthly_report_data.xml',
        'report/weekly_report_template.xml',    # <-- MOVED HERE
        'report/monthly_report_template.xml',   # <-- MOVED HERE
    ],
    'assets': {
        'web.assets_backend': [
            'smarten_ai/static/src/js/occupancy_dashboard.js',
            # 'smarten_ai/views/portal_templates.xml',   # keep commented (optional)
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}