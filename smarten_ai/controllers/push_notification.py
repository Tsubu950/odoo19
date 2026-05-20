import requests
from odoo import http, fields
from odoo.http import request

def send_push_notification(user_ids, title, body, data=None):
    if not user_ids:
        return
    employees = request.env['hr.employee'].sudo().search([('user_id', 'in', user_ids)])
    tokens = [e.firebase_token for e in employees if e.firebase_token]
    if not tokens:
        return
    api_key = request.env['ir.config_parameter'].sudo().get_param('smarten_ai.fcm_api_key')
    if not api_key:
        return
    headers = {'Authorization': f'key={api_key}', 'Content-Type': 'application/json'}
    payload = {
        'registration_ids': tokens,
        'notification': {'title': title, 'body': body},
        'data': data or {},
        'priority': 'high',
    }
    try:
        requests.post('https://fcm.googleapis.com/fcm/send', json=payload, headers=headers, timeout=3)
    except Exception:
        pass