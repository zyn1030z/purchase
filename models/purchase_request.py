# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = "Purchase Request"
    name = fields.Char(string='Số phiếu', defalt='/', readonly=False)

    # request_by = fields.Char(string='Người yêu cầu', default=lambda self: self.env.user.name)
    request_by = fields.Many2one('res.users', 'Người yêu cầu', default=lambda self: self.env.user)
    # check_by = fields.Char(string='Người duyệt')
    check_by = fields.Many2one('res.users', 'Người duyệt', default=lambda self: self.env.user)
    department = fields.Char(string='Bộ phận')
    cost_total = fields.Char(string='Tổng chi phí')
    creation_date = fields.Date(string='Ngày yêu cầu', default=datetime.today())
    due_date = fields.Date(string='Ngày cần cấp')
    approved_date = fields.Date(string='Ngày phê duyệt')
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('waiting_for_approval', 'Chờ duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('complete', 'Hoàn thành'),
        ('cancel', 'Hủy')],
        string='Tình trạng sử dụng', default='draft', track_visibility='always')
    company = fields.Char(string='Công ty', readonly=True)
    reject_reason = fields.Char(string='Lý do từ chối duyệt')

    # room_booking_ids = fields.One2many('purchase.request.line', 'room_booking_id', string='Danh sách phòng')
    @api.depends('creation_date')
    def __compute_purchase_request_sequence_number_next(self):
        pass

    @api.model
    def create(self, vals_list):
        vals_list = {'name': 'test'}
        obj = super(PurchaseRequest, self).create(vals_list)
        # if obj.name == '/':
        #     number = 'test'
        #     obj.write({'name': number})
        return obj
