from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route('/test', type='http', auth='none')
    def books(self):
        records = request.env['purchase.request'].sudo().search([('request_by', '=', 8)])
        print(records.mapped('name'))
        result = '<html><body><table><tr><td>'
        result += '</td></tr><tr><td>'.join(records.mapped('name'))
        return result


