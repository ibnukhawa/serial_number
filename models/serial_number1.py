from odoo import api, models, fields, models, _
import math
import re
from datetime import datetime,timedelta,time

class SerialNumber1(models.Model):
    _name = "serial.number1"
    _description = "Serial Number"

    name = fields.Char(string='Serial Number',  copy=False,  index=True, default=lambda self: _('New'))
    sale_id = fields.Many2one('sale.order', string='SO Reference')
    partner_id = fields.Many2one('res.partner',string='Customer', track_visibility='onchange', related='sale_id.partner_id')
    date = fields.Date(string='Tanggal',default=fields.Date.today())
    qty_id = fields.Integer(string="Qty", required=True, default='1')
    serial_number_note = fields.Text(string='Note')
    product_id = fields.Many2one('product.product', string='Product', related='sale_id.product_id', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, domain="[('type','=','normal')]",
        required=True, help="Select category for the current product", related='product_id.categ_id')
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', copy=True, filter_domain="[('order_line.sale_id','ilike',self)]")
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('serial.number1') 
        values['name'] = seq
        result = super(SerialNumber1,self).create(values)
        return result