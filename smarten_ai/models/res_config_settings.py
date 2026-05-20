from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fcm_api_key = fields.Char(string='Firebase API Key', config_parameter='smarten_ai.fcm_api_key')
    fcm_sender_id = fields.Char(string='Firebase Sender ID', config_parameter='smarten_ai.fcm_sender_id')
    telegram_bot_token = fields.Char(string='Telegram Bot Token', config_parameter='smarten_ai.telegram_bot_token')
    default_telegram_chat_id = fields.Char(string='Default Telegram Chat ID', config_parameter='smarten_ai.default_telegram_chat_id')
    api_key = fields.Char(string='API Key', config_parameter='smarten_ai.api_key', default='b7b52ab57c4838241cc2ca7d8c3d8715fe41dcdc')
    auto_close_hours = fields.Integer(string='Auto‑close stale sessions (hours)', config_parameter='smarten_ai.auto_close_hours', default=12)
    duplicate_cooldown_sec = fields.Integer(string='Duplicate event cooldown (seconds)', config_parameter='smarten_ai.duplicate_cooldown_sec', default=5)
    notify_vip = fields.Boolean(string='Notify on VIP entry', config_parameter='smarten_ai.notify_vip', default=True)
    notify_blocked = fields.Boolean(string='Notify on Blocked entry', config_parameter='smarten_ai.notify_blocked', default=True)