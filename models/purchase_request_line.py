from odoo import fields, models, api


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = "Purchase Request"
    _inherit = [
        'mail.thread'
    ]
    product_id = fields.Many2one('product.product', string='Sản phẩm', change_default=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes',
                                domain=['|', ('active', '=', False), ('active', '=', True)])
    unit_measure = fields.Char(string='Đơn vị tính', required=True, default='Cái')
    product_qty = fields.Integer(string='Số lượng yêu cầu', digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string='Đơn giá dự kiến', required=True, digits='Product Price')
    price_subtotal = fields.Float(string='Chi phí dự kiến', compute='_compute_amount')
    due_date = fields.Date(string='Ngày cần cấp')
    description = fields.Text(string='Ghi chú')
    delivered_qty = fields.Float(string='Số lượng đã mua')
    # order_request_id = fields.Many2one('purchase.request', string='Purchase Request Reference',
    #                            ondelete='cascade')
    order_request_id = fields.Many2one(comodel_name='purchase.request', string='Purchase Request Reference',
                                       ondelete='cascade')

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            total = line.product_qty * line.price_unit
            line.price_subtotal = total

    @api.onchange('product_id')
    def test(self):
        if not self.product_id:
            return
        print('test onchange')
