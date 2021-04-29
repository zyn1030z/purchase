from odoo import models, fields


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _inherit = 'purchase.order'
    test = fields.Char(string='Test')
    test1 = fields.Char(string='Test1')
    test2 = fields.Char(string='Test2')
