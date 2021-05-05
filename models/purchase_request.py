# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = "Purchase Request"
    _inherit = ['mail.thread']
    name = fields.Char('Code', readonly=True, select=True, copy=False, default='New ')
    request_by = fields.Many2one('res.users', 'Request User', default=lambda self: self.env.user)
    check_by = fields.Many2one('res.users', 'Approved User', default=lambda self: self.env.user)
    department = fields.Many2one('hr.department', "Department",
                                 default=lambda self: self.env.user.employee_ids.department_id)
    cost_total = fields.Char(string='Total cost', compute='_amount_all')
    creation_date = fields.Date(string='Request Date', default=datetime.today())
    due_date = fields.Date(string='Due date')
    approved_date = fields.Date(string='Approved Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting for approval'),
        ('approved', 'Approved'),
        ('complete', 'Completed'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel')],
        string='Use status', default='draft', track_visibility='always')
    # company = fields.Char(string='Company', readonly=False)
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id,
        readonly=1
    )
    reject_reason = fields.Char(string='Rejection Reason')
    # order_request_line = fields.One2many('purchase.request.line', 'order_request_id', string='Order Lines', copy=True)
    order_request_line = fields.One2many(comodel_name='purchase.request.line', inverse_name='order_request_id',
                                         string='Order Lines', )

    reject_reason_request1 = fields.Char(compute='reject_function', string='Rejection reason')

    # reject_reason_request = fields.Char(related='reject_reason_id.reason_reject_reason')

    # @api.model
    # def create(self, vals_list):
    #     # vals_list = {'name': 'test'}
    #     obj = super(PurchaseRequest, self).create(vals_list)
    #     if obj.name == '/':
    #         # number = 'PR.200806.0001'
    #         # obj.write({'name': number})
    #         # sequence_id = self.env['purchase.request'].search([('code', '=', 'your.sequence.code')])
    #         sequence_pool = self.env['ir.sequence']
    #         print('sequence_pool', sequence_pool)
    #
    #         d_to = datetime.today()
    #         # name = 'PR.200806.0001'
    #         name = 'PR.' + str(d_to.year)[-2:] + str(d_to.month) + str(d_to.day)
    #         print(name)
    #         obj.write({'name': name})
    #     return obj
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('purchase.request.seq') or '/'
        d_to = datetime.today()
        name = 'PR.' + str(d_to.year)[-2:] + str(d_to.month) + str(d_to.day)
        print(type(seq))
        vals['name'] = name + '.' + seq
        return super(PurchaseRequest, self).create(vals)

    @api.depends('order_request_line.price_subtotal')
    def _amount_all(self):
        for order in self:
            amount_total = 0
            for line in order.order_request_line:
                amount_total += line.price_subtotal
            order.cost_total = amount_total

    def send_approve_purchase_request(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def approve_purchase_request(self):
        for rec in self:
            rec.state = 'approved'

    def reject_purchase_request(self):
        for rec in self:
            rec.state = 'draft'
            # print('test reject', self.id)
            # print(self.env['reject.reason'].search([('owner_id', '=', 96)]))
            # return {
            #     'type': 'ir.actions.act_window',
            #     'name': 'Lý do từ chối',
            #     'res_model': 'reject.reason',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'target': 'new',
            # }
            return {
                'name': 'Reject Reason',
                'type': 'ir.actions.act_window',
                'res_model': 'reject.reason',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new'
            }

    def approved_function(self):
        for rec in self:
            rec.state = 'complete'

    def cancel_function(self):
        for rec in self:
            rec.state = 'cancel'

    def reject_function(self):
        for rc in self:
            reject = self.env['reject.reason'].search([('owner_id', '=', self.id)]).reason_reject_reason
            rc.reject_reason_request1 = reject
