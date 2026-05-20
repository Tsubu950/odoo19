from odoo import http, fields
from odoo.http import request
import base64
import logging

_logger = logging.getLogger(__name__)

class GymAIController(http.Controller):

    @http.route('/api/gym/monitor', type='json', auth='none', methods=['POST'], csrf=False)
    def monitor(self):
        # API Key check
        api_key = request.httprequest.headers.get('Authorization')
        if api_key != "Bearer 72847ee8d6c2a82914b1641a1dc30d36a5e49320":
            return {'status': 'unauthorized'}

        data = request.get_json_data()
        if not data:
            return {'status': 'error', 'message': 'No JSON data'}

        person_name = data.get('person_id')
        camera_source = data.get('camera_source')
        image_b64 = data.get('image')
        gender = data.get('gender')
        age_range = data.get('age_range')
        tracking_id = data.get('tracking_id')
        guest_id = data.get('guest_id')

        # --- CASE 1: Member / Staff (has person_name) ---
        if person_name:
            person = request.env['gym.person'].sudo().search([('name', 'ilike', person_name)], limit=1)
            if not person:
                return {'status': 'error', 'message': f'Person "{person_name}" not found'}
            direction = 'IN' if camera_source == 'entry' else 'OUT'
            request.env['gym.attendance.log'].sudo().create({
                'person_id': person.id,
                'direction': direction,
                'camera_source': camera_source,
                'person_type': person.role,
                'timestamp': fields.Datetime.now(),
            })
            return {'status': 'attendance_recorded', 'person': person.name}

        # --- CASE 2: Guest (has guest_id and image) ---
        if guest_id and image_b64:
            request.env['gym.guest.log'].sudo().create({
                'guest_id': guest_id,
                'image': image_b64,
                'gender': gender or 'Unknown',
                'age_range': age_range or 'Unknown',
                'camera_source': camera_source,
                'timestamp': fields.Datetime.now(),
            })
            return {'status': 'guest_logged'}

        # --- CASE 3: Covered face (has tracking_id and image) ---
        if tracking_id and image_b64:
            request.env['gym.covered.log'].sudo().create({
                'tracking_id': str(tracking_id),
                'image': image_b64,
                'gender': gender or 'Unknown',
                'age_range': age_range or 'Unknown',
                'camera_source': camera_source,
                'reason': 'face_not_visible',
                'timestamp': fields.Datetime.now(),
            })
            return {'status': 'covered_logged'}

        return {'status': 'error', 'message': 'Missing required data'}