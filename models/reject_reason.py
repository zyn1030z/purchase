from datetime import datetime

from odoo import models, fields, api


class RejectReason(models.TransientModel):
    _name = 'reject.reason'
    _description = 'Reject Reason'
    date_reject_reason = fields.Date(string='Date', default=datetime.today())
    reason_reject_reason = fields.Text(string='Reason', required=True)
    owner_id = fields.Many2one('purchase.request', default=lambda self: self.env['purchase.request'].browse(
        self.env.context.get('active_id')))

    @api.model
    def create(self, vals_list):
        return super(RejectReason, self).create(vals_list)
