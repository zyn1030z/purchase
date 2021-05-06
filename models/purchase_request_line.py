from odoo import fields, models, api


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = "Purchase Request"
    _inherit = [
        'mail.thread'
    ]
    product_id = fields.Many2one('product.product', string='Product', change_default=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes',
                                domain=['|', ('active', '=', False), ('active', '=', True)])
    unit_measure = fields.Char(string='Measure Unit', required=True, default='PCS', readonly=1)
    product_qty = fields.Integer(string='Quantity Product', digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    price_subtotal = fields.Float(string='Subtotal Price', compute='_compute_amount')
    due_date = fields.Date(string='Due date',
                           related='order_request_id.due_date')
    description = fields.Text(string='Description')
    delivered_qty = fields.Float(string='Quantity delivered')

    # order_request_id = fields.Many2one('purchase.request', string='Purchase Request Reference',
    #                            ondelete='cascade')
    order_request_id = fields.Many2one(comodel_name='purchase.request', string='Purchase Request Reference',
                                       ondelete='cascade')
    state = fields.Char('Use status', compute="_compute_state")

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            total = line.product_qty * line.price_unit
            line.price_subtotal = total

    @api.depends('order_request_id.due_date')
    def _depends_due_date(self):
        for rec in self:
            if rec.order_request_id.due_date:
                rec.due_date = rec.order_request_id.due_date

    def _compute_state(self):
        print(self.order_request_id)
        self.state = self.order_request_id.state
        # state_pr = self.env['purchase.request.line'].search([('order_request_id', '=', self.id)]).state
        # print(state_pr)
        # rec.state = state_pr
