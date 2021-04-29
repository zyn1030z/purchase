from odoo import models, fields


class PurchaseRequest(models.Model):
    _inherit = 'purchase.order'
    test = fields.Char(string='Test')
