from odoo import http, fields
from odoo.http import request
import logging


_logger = logging.getLogger(__name__)

class OmniAIController(http.Controller):

    @http.route('/api/omni/monitor', type='json', auth='none', methods=['POST'], csrf=False)
    def monitor(self):
        # 1. API Key authentication
        api_key = request.httprequest.headers.get('Authorization')
        if api_key != "Bearer b7b52ab57c4838241cc2ca7d8c3d8715fe41dcdc":
            _logger.warning("Unauthorized API access attempt")
            return {'status': 'unauthorized'}

        # 2. Get JSON data (plain JSON, not JSON-RPC)
        data = request.get_json_data()
        if not data:
            return {'status': 'error', 'message': 'No JSON data'}

        # Extract fields
        employee_name = data.get('employee_id')   # can be name (string) or ID (int)
        direction = data.get('direction')
        camera_source = data.get('camera_source')
        image_b64 = data.get('image')
        gender = data.get('gender')
        age_range = data.get('age_range')
        unknown_id = data.get('unknown_id')
        tracking_id = data.get('tracking_id')
        timestamp = fields.Datetime.now()

        # ------------------------------
        # 3. Employee (staff/owner/VIP/blocked)
        # ------------------------------
        if employee_name:
            # Look up employee by name (case-insensitive)
            employee = request.env['hr.employee'].sudo().search([('name', 'ilike', employee_name)], limit=1)
            if not employee:
                return {'status': 'error', 'message': f'Employee "{employee_name}" not found'}

            # Create standard attendance record
            attendance = request.env['hr.attendance'].sudo().create({
                'employee_id': employee.id,
                'check_in': timestamp if direction == 'IN' else False,
                'check_out': timestamp if direction == 'OUT' else False,
            })

            # Additional logging based on flags
            if employee.is_blocked:
                request.env['omni.blocked.log'].sudo().create({
                    'employee_id': employee.id,
                    'direction': direction,
                    'camera_source': camera_source,
                    'entry_time': timestamp if direction == 'IN' else False,
                    'exit_time': timestamp if direction == 'OUT' else False,
                    'photo': image_b64,
                    'alert_sent': True,
                })
                _logger.warning(f"BLOCKED PERSON ENTRY: {employee.name}")
            elif employee.is_vip:
                request.env['omni.vip.log'].sudo().create({
                    'employee_id': employee.id,
                    'direction': direction,
                    'camera_source': camera_source,
                    'entry_time': timestamp if direction == 'IN' else False,
                    'exit_time': timestamp if direction == 'OUT' else False,
                    'photo': image_b64,
                    'gender': gender,
                    'age_range': age_range,
                })
                _logger.info(f"VIP ENTRY: {employee.name}")
            # For normal employees, no extra log
            return {'status': 'attendance_recorded', 'person': employee.name}

        # ------------------------------
        # 4. Unknown person
        # ------------------------------
        if unknown_id:
            request.env['omni.unknown.log'].sudo().create({
                'unknown_id': unknown_id,
                'direction': direction,
                'camera_source': camera_source,
                'entry_time': timestamp if direction == 'IN' else False,
                'exit_time': timestamp if direction == 'OUT' else False,
                'gender': gender,
                'age_range': age_range,
                'photo': image_b64,
            })
            return {'status': 'unknown_logged'}

        # ------------------------------
        # 5. Covered face
        # ------------------------------
        if tracking_id:
            request.env['omni.covered.log'].sudo().create({
                'tracking_id': str(tracking_id),
                'direction': direction,
                'camera_source': camera_source,
                'entry_time': timestamp if direction == 'IN' else False,
                'exit_time': timestamp if direction == 'OUT' else False,
                'photo': image_b64,
            })
            return {'status': 'covered_logged'}

        return {'status': 'error', 'message': 'Missing required fields'}