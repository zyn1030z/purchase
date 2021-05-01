# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class PurchaseRequest(models.Model):
    _name = 'purchase.request'

    name = fields.Char(string='Số phiếu', required=True)
    request_by = fields.Char(string='người yêu cầu')
    department = fields.Char(string='Bộ phận')
    cost_total = fields.Char(string='Tổng chi phí')
    creation_date = fields.Date(string='ngày yêu cầu', required=True)
    due_date = fields.Date(string='ngày cần cấp', required=True)
    approved_date = fields.Date(string='ngày phê duyệt', required=True)
    state = fields.Selection([('booking', 'Đang đợi'), ('in_use', 'Đang sử dụng'), ('paid', 'Đã thanh toán')],
                             string='Tình trạng sử dụng')
    company = fields.Char(string='công ty')
    reject_reason = fields.Char(string='lý do từ chối duyệt')

    # room_booking_ids = fields.One2many('purchase.request.line', 'room_booking_id', string='Danh sách phòng')
