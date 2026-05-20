import requests
import json
from odoo import http
from odoo.http import request

def send_telegram_message(chat_id, text):
    token = request.env['ir.config_parameter'].sudo().get_param('smarten_ai.telegram_bot_token')
    if not token or not chat_id:
        return
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=2)
    except Exception as e:
        _logger.warning(f"Telegram send failed: {e}")

class TelegramBotController(http.Controller):
    @http.route('/api/smarten/telegram/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def webhook(self):
        data = json.loads(request.httprequest.data)
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        if text == '/status':
            occ = request.env['smarten.occupancy.snapshot'].sudo().search([], limit=1, order='timestamp desc')
            msg = f"Current occupancy: {occ.total_occupancy if occ else 0}"
            send_telegram_message(chat_id, msg)
        return ''