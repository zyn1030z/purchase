# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime

from odoo.exceptions import UserError, ValidationError
import base64
import xlrd


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = "Purchase Request"
    _inherit = ['mail.thread']
    name = fields.Char('Code', readonly=True, select=True, copy=False, default='New')
    request_by = fields.Many2one('res.users', 'Request User', default=lambda self: self.env.user)
    check_by = fields.Many2one('res.users', 'Approved User', default=lambda self: self.env.user)
    department = fields.Many2one('hr.department', "Department",
                                 default=lambda self: self.env.user.department_id)
    cost_total = fields.Integer(string='Total cost', compute='_amount_all')
    creation_date = fields.Date(string='Request Date', default=datetime.today())
    due_date = fields.Date(string='Due date')
    approved_date = fields.Date(string='Approved Date', readonly=1)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting for approval'),
        ('approved', 'Approve'),
        ('complete', 'Complete'),
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
    context = fields.Text(default='{}', required=True)

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
        vals['name'] = name + '.' + seq
        return super(PurchaseRequest, self).create(vals)

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Purchase Request'),
            'template': 'purchase_request/static/xls/imp_donmuahang.xls'
        }]

    @api.depends('order_request_line.price_subtotal')
    def _amount_all(self):
        # print(self)
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
            rec.approved_date = datetime.today()

    def reject_purchase_request(self):
        for rec in self:
            rec.state = 'reject'
            # print('test reject', self.id)
            # print(self.env['reject.reason'].search([('owner_id', '=', 96)]))

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

    def redirect_draft(self):
        for rec in self:
            rec.state = 'draft'

    def cancel_function(self):
        for rec in self:
            rec.state = 'cancel'

    def reject_function(self):
        for rc in self:
            reject = self.env['reject.reason'].search([('owner_id', '=', self.id)],
                                                      order="id desc", limit=1).reason_reject_reason
            rc.reject_reason_request1 = reject

    # @api.constrains('order_request_line')
    # def _check_exist_product_in_line(self):
    #     for purchase in self:
    #         exist_product_list = []
    #         for line in purchase.order_request_line:
    #             if line.product_id.id in exist_product_list:
    #                 raise ValidationError('Product must be one per line.')
    #             exist_product_list.append(line.product_id.id)

    # Construct file excel : Product,Quantity,Product,Unit,Price,Description
    xls_file = fields.Binary('Import Detail')

    def import_xls(self):
        try:
            wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        except:
            raise ValidationError(
                'File import phải là file excel')
        product_id_in_datas = self.env['purchase.request.line'].search(
            [('order_request_id', '=', self.id)]).product_id  # product_id trong database
        # mã sản phẩm trong data base
        exist_product_list = []
        # mã code trong file excel
        exist_code_list = []
        for product_id_in_data in product_id_in_datas:
            exist_product_list.append(product_id_in_data.id)
        for sheet in wb.sheets():
            arr_line_error_slsp = []
            arr_line_error_not_exist_database = []
            values = []
            line_check_exist_data = 7
            line_check_slsp = 7

            for row in range(sheet.nrows):
                col_values = []
                for col in range(sheet.ncols):
                    value = sheet.cell(row, col).value
                    try:
                        value = str(value)
                    except:
                        pass
                    col_values.append(value)
                values.append(col_values)
            # kiểm tra số sp k tồn tại trong database
            for val in values[6:]:
                product_id_import = self.env['product.product'].search(
                    [('default_code', '=', val[0])]).id  # product_id trong file import
                if product_id_import is False:
                    arr_line_error_not_exist_database.append(line_check_exist_data)
                line_check_exist_data += 1

            # kiểm tra số lượng sản phẩm lớn hơn 0
            for val in values[6:]:
                if not val[3]:
                    arr_line_error_slsp.append(line_check_slsp)
                elif float(val[3]) < 0:
                    arr_line_error_slsp.append(line_check_slsp)
                line_check_slsp += 1

            # kiểm tra đơn vị tính
            arr_line_error_dvt = []
            line_check_dvt = 7
            for val in values[6:]:
                print(val)
                if not val[2]:
                    # kiểm tra nếu k có đơn vị tính thì gán theo hệ thống
                    product_id_import_standard = self.env['product.product'].search(
                        [('default_code', '=', val[0])]).product_tmpl_id.id
                    uom = self.env['product.template'].search(
                        [('id', '=', product_id_import_standard)]
                    ).uom_id
                    val[2] = uom.name
                    line_check_dvt += 1
                elif val[2]:
                    arr_dvt = self.env['uom.uom'].search([('name', '=', val[2])])
                    if len(arr_dvt) == 0:
                        arr_line_error_dvt.append(line_check_dvt)
                    line_check_dvt += 1
            listToStr_line_slsp = ' , '.join([str(elem) for elem in arr_line_error_slsp])
            listToStr_line_not_exist_database = ' , '.join([str(elem) for elem in arr_line_error_not_exist_database])
            listToStr_line_dvt = ' , '.join([str(elem) for elem in arr_line_error_dvt])
            if len(arr_line_error_not_exist_database) == 0 and len(arr_line_error_dvt) == 0 and len(
                    arr_line_error_slsp) == 0:
                for val in values[6:]:
                    if not val[4]:
                        # lấy đơn giá rồi gán vào val[4]
                        product_id_import_standard = self.env['product.product'].search(
                            [('default_code', '=', val[0])]).product_tmpl_id.id
                        standard_price = self.env['product.template'].search(
                            [('id', '=', product_id_import_standard)]
                        ).standard_price
                        val[4] = standard_price
                    product_id_import = self.env['product.product'].search(
                        [('default_code', '=', val[0])]).id
                    self.env['purchase.request.line'].create(
                        {'price_unit': float(val[4]), 'product_qty': float(val[3]), 'order_request_id': self.id,
                         'product_id': product_id_import, 'unit_measure': val[2]})
                    self.env.cr.commit()
            elif len(arr_line_error_not_exist_database) != 0 and len(arr_line_error_dvt) == 0 and len(
                    arr_line_error_slsp) == 0:
                raise ValidationError(
                    _('Sản phẩm đã tồn tại trong hệ thống, dòng (%s)') % str(listToStr_line_not_exist_database))
            elif len(arr_line_error_not_exist_database) != 0 and len(arr_line_error_dvt) != 0 and len(
                    arr_line_error_slsp) == 0:
                raise ValidationError(
                    _('Sản phẩm đã tồn tại trong hệ thống, dòng (%s)\n'
                      'Đơn vị tính của sản phẩm phải cùng nhóm đơn vị tính đã khai báo, dòng (%s)') % (str(
                        listToStr_line_not_exist_database), str(
                        listToStr_line_dvt)))
            elif len(arr_line_error_not_exist_database) != 0 and len(arr_line_error_dvt) != 0 and len(
                    arr_line_error_slsp) != 0:
                raise ValidationError(
                    _('Sản phẩm đã tồn tại trong hệ thống, dòng (%s)\n'
                      'Đơn vị tính của sản phẩm phải cùng nhóm đơn vị tính đã khai báo, dòng (%s)\n'
                      'Số lượng sản phẩm phải lớn hơn 0 hoặc không để trống, dòng (%s)')
                    % (str(listToStr_line_not_exist_database),
                       str(listToStr_line_dvt),
                       str(listToStr_line_slsp)))
            elif len(arr_line_error_not_exist_database) == 0 and len(arr_line_error_dvt) != 0 and len(
                    arr_line_error_slsp) == 0:
                raise ValidationError(
                    _('Đơn vị tính của sản phẩm phải cùng nhóm đơn vị tính đã khai báo, dòng (%s)') % str(
                        listToStr_line_dvt))
            elif len(arr_line_error_not_exist_database) == 0 and len(arr_line_error_dvt) == 0 and len(
                    arr_line_error_slsp) != 0:
                raise ValidationError(
                    _('Số lượng sản phẩm phải lớn hơn 0 hoặc không để trống, dòng (%s)') % str(listToStr_line_slsp))
            elif len(arr_line_error_not_exist_database) == 0 and len(arr_line_error_dvt) != 0 and len(
                    arr_line_error_slsp) != 0:
                raise ValidationError(
                    _(
                        'Số lượng sản phẩm phải lớn hơn 0 hoặc không để trống, dòng (%s)\n'
                        'Đơn vị tính của sản phẩm phải cùng nhóm đơn vị tính đã khai báo, dòng (%s)') % (str(
                        listToStr_line_slsp), str(listToStr_line_dvt)))
            elif len(arr_line_error_not_exist_database) != 0 and len(arr_line_error_dvt) == 0 and len(
                    arr_line_error_slsp) != 0:
                raise ValidationError(
                    _('Sản phẩm đã tồn tại trong hệ thống, dòng (%s)\n'
                      'Số lượng sản phẩm phải lớn hơn 0 hoặc không để trống, dòng (%s)')
                    % (str(listToStr_line_not_exist_database),
                       str(listToStr_line_slsp)))
