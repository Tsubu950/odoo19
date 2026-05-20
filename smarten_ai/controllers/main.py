from odoo import http, fields
from odoo.http import request
import base64
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class SmartenAIController(http.Controller):

    @http.route('/api/smarten/monitor', type='json', auth='none', methods=['POST'], csrf=False)
    def monitor(self):
        api_key = request.httprequest.headers.get('Authorization')
        expected_key = request.env['ir.config_parameter'].sudo().get_param('smarten_ai.api_key', 'b7b52ab57c4838241cc2ca7d8c3d8715fe41dcdc')
        if api_key != f"Bearer {expected_key}":
            return {'status': 'unauthorized'}

        data = request.jsonrequest
        if not data:
            return {'status': 'error', 'message': 'No JSON data'}

        # Fields from AI bridge
        person_name = data.get('person_id')
        person_type = data.get('person_type')
        direction = data.get('direction')
        camera_source = data.get('camera_source')
        unknown_id = data.get('unknown_id')
        tracking_id = data.get('tracking_id')
        image_b64 = data.get('image')
        gender = data.get('gender')
        age_range = data.get('age_range')
        liveness_score = data.get('liveness_score')
        reid_embedding = data.get('reid_embedding')
        timestamp = fields.Datetime.now()

        # Cooldown check (prevent duplicates)
        cooldown_sec = int(request.env['ir.config_parameter'].sudo().get_param('smarten_ai.duplicate_cooldown_sec', 5))

        # 1. Known employee (staff/owner/vip/blocked)
        if person_name:
            employee = request.env['hr.employee'].sudo().search([('name', 'ilike', person_name)], limit=1)
            if not employee:
                return {'status': 'error', 'message': f'Employee "{person_name}" not found'}

            # Check last attendance for cooldown
            last_att = request.env['smarten.attendance.log'].sudo().search([
                ('person_id', '=', employee.id),
                ('direction', '=', direction),
                ('timestamp', '>', fields.Datetime.now() - timedelta(seconds=cooldown_sec))
            ], limit=1)
            if last_att:
                return {'status': 'ignored_cooldown'}

            # Create attendance record in hr.attendance
            att = request.env['hr.attendance'].sudo().create({
                'employee_id': employee.id,
                'check_in': timestamp if direction == 'IN' else False,
                'check_out': timestamp if direction == 'OUT' else False,
            })
            # Store additional data in custom log
            log_vals = {
                'person_id': employee.id,
                'direction': direction,
                'camera_source': camera_source,
                'entry_time': timestamp if direction == 'IN' else False,
                'exit_time': timestamp if direction == 'OUT' else False,
                'person_type': employee.role or 'staff',
                'liveness_score': liveness_score,
                'reid_embedding': reid_embedding,
                'photo': image_b64,
            }
            log = request.env['smarten.attendance.log'].sudo().create(log_vals)

            # Handle VIP / Blocked alerts
            if employee.is_vip and direction == 'IN':
                request.env['smarten.vip.log'].sudo().create({
                    'employee_id': employee.id,
                    'direction': direction,
                    'camera_source': camera_source,
                    'entry_time': timestamp,
                    'photo': image_b64,
                    'gender': gender,
                    'age_range': age_range,
                })
                self._send_notification(employee, 'VIP Entry', f'VIP {employee.name} entered')
            elif employee.is_blocked:
                request.env['smarten.blocked.log'].sudo().create({
                    'employee_id': employee.id,
                    'direction': direction,
                    'camera_source': camera_source,
                    'entry_time': timestamp,
                    'photo': image_b64,
                    'alert_sent': True,
                })
                self._send_notification(employee, 'BLOCKED PERSON', f'Blocked person {employee.name} attempted entry')

            return {'status': 'attendance_recorded', 'person': employee.name}

        # 2. Unknown person (face visible, not in DB)
        if unknown_id and image_b64:
            # Check cooldown for same unknown_id and direction
            last_unknown = request.env['smarten.unknown.log'].sudo().search([
                ('unknown_id', '=', unknown_id),
                ('direction', '=', direction),
                ('timestamp', '>', fields.Datetime.now() - timedelta(seconds=cooldown_sec))
            ], limit=1)
            if last_unknown:
                return {'status': 'ignored_cooldown'}

            request.env['smarten.unknown.log'].sudo().create({
                'unknown_id': unknown_id,
                'direction': direction,
                'camera_source': camera_source,
                'entry_time': timestamp if direction == 'IN' else False,
                'exit_time': timestamp if direction == 'OUT' else False,
                'gender': gender or 'Unknown',
                'age_range': age_range or 'Unknown',
                'photo': image_b64,
                'liveness_score': liveness_score,
                'reid_embedding': reid_embedding,
            })
            return {'status': 'unknown_logged'}

        # 3. Covered face (no face detected)
        if tracking_id and image_b64:
            last_covered = request.env['smarten.covered.log'].sudo().search([
                ('tracking_id', '=', tracking_id),
                ('direction', '=', direction),
                ('timestamp', '>', fields.Datetime.now() - timedelta(seconds=cooldown_sec))
            ], limit=1)
            if last_covered:
                return {'status': 'ignored_cooldown'}

            request.env['smarten.covered.log'].sudo().create({
                'tracking_id': str(tracking_id),
                'direction': direction,
                'camera_source': camera_source,
                'entry_time': timestamp if direction == 'IN' else False,
                'exit_time': timestamp if direction == 'OUT' else False,
                'photo': image_b64,
                'reid_embedding': reid_embedding,
            })
            return {'status': 'covered_logged'}

        return {'status': 'error', 'message': 'Missing required fields'}

    def _send_notification(self, employee, title, message):
        # Push notification via FCM
        if employee.firebase_token:
            push_notification.send_push_notification([employee.user_id.id], title, message)
        # Telegram bot
        if employee.telegram_chat_id:
            telegram_bot.send_telegram_message(employee.telegram_chat_id, f"{title}\n{message}")