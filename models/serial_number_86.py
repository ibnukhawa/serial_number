from odoo import api, models, fields, models, _
import math
import re
from datetime import datetime,timedelta,time

class SerialNumber86(models.Model):
    _name = "serial.number86"
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
        seq = self.env['ir.sequence'].get('serial.number86') 
        values['name'] = seq
        result = super(SerialNumber86,self).create(values)
        return result
    
    # @api.model
    # def create(self, vals):
    #     res = super(ProductAutoBarcode, self).create(vals)
    #     ean = generate_ean(str(res.id))
    #     res.barcode = ean
    #     return res


    # def ean_checksum(eancode):
    #     """returns the checksum of an ean string of length 13, returns -1 if the string has the wrong length"""
    #     if len(eancode) != 13:
    #         return -1
    #     oddsum = 0
    #     evensum = 0
    #     eanvalue = eancode
    #     reversevalue = eanvalue[::-1]
    #     finalean = reversevalue[1:]

    #     for i in range(len(finalean)):
    #         if i % 2 == 0:
    #             oddsum += int(finalean[i])
    #         else:
    #             evensum += int(finalean[i])
    #     total = (oddsum * 3) + evensum

    #     check = int(10 - math.ceil(total % 10.0)) % 10
    #     return check


    # def check_ean(eancode):
    #     """returns True if eancode is a valid ean13 string, or null"""
    #     if not eancode:
    #         return True
    #     if len(eancode) != 13:
    #         return False
    #     try:
    #         int(eancode)
    #     except:
    #         return False
    #     return ean_checksum(eancode) == int(eancode[-1])


    # def generate_ean(ean):
    #     """Creates and returns a valid ean13 from an invalid one"""
    #     if not ean:
    #         return "0000000000000"
    #     ean = re.sub("[A-Za-z]", "0", ean)
    #     ean = re.sub("[^0-9]", "", ean)
    #     ean = ean[:13]
    #     if len(ean) < 13:
    #         ean = ean + '0' * (13 - len(ean))
    #     return ean[:-1] + str(ean_checksum(ean))