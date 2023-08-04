from odoo import http
from odoo.http import request


class Api(http.Controller):
    @http.route('/sms_server/sms/add', auth="public", type="json")
    def sms_add(self, **data):
        try:
            partner = request.env['res.partner'].sudo().search([('sms_token', '=', data['sms_token'])])
            if not partner:
                return {'ok': False, 'message': 'Invalid Token'}
            request.env['sms_server.queue'].sudo().create({
                'partner': partner.id,
                'phone': data['phone'],
                'message': data['message'],
            })
            return {'ok': True, 'message': 'SMS added to the queue.'}
        except Exception as e:
            print(e)
            return {'ok': False, 'message': e}

    @http.route('/sms_server/sms/read/<string:sms_token>', auth="public", type="json")
    def sms_read(self, **data):
        try:
            partner = request.env['res.partner'].sudo().search([('sms_token', '=', data['sms_token'])])
            if not partner:
                return {'ok': False, 'message': 'Invalid Token'}
            sms_queues = request.env['sms_server.queue'].sudo().search([('partner', '=', partner.id)])
            queue_data = []
            for sms_queue in sms_queues:
                queue_data.append({
                    'id': sms_queue.id,
                    'phone': sms_queue.phone,
                    'message': sms_queue.message
                })
            return {'ok': True, 'data': queue_data}
        except Exception as e:
            print(e)
            return {'ok': False, 'message': e}

    @http.route('/sms_server/sms/delete/<string:sms_token>/<int:sms_id>', auth="public", type="json")
    def sms_delete(self, sms_token, sms_id, **data):
        try:
            partner = request.env['res.partner'].sudo().search([('sms_token', '=', sms_token)])
            if not partner:
                return {'ok': False, 'message': 'Invalid Token'}
                # Search for the SMS queue record with the provided sms_id
            sms_queue = request.env['sms_server.queue'].sudo().browse(sms_id)
            if not sms_queue or sms_queue.partner.id != partner.id:
                return {'ok': False, 'message': 'Invalid SMS ID or SMS not associated with the provided token'}
            sms_queue.unlink()
            return {'ok': True, 'message': 'Delete SMS from queue'}
        except Exception as e:
            print(e)
            return {'ok': False, 'message': e}
