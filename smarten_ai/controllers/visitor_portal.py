from odoo import http
from odoo.http import request
import base64

class VisitorPortal(http.Controller):

    @http.route('/api/smarten/visitor/register', type='http', auth='public', methods=['POST'], csrf=False)
    def visitor_register(self, **post):
        name = post.get('name')
        email = post.get('email')
        visit_date = post.get('visit_date')
        face_file = post.get('face_image')
        if not name or not visit_date or not face_file:
            return "Missing required fields"
        image_data = face_file.read()
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        visitor = request.env['smarten.visitor.pre_registration'].sudo().create({
            'visitor_name': name,
            'email': email,
            'visit_date': visit_date,
            'face_image': image_b64,
        })
        return f"Registration successful. Your token: {visitor.token}"