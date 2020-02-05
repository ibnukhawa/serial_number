from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'    
    _name = "sale.order"
     
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', copy=True)
    product_id = fields.Many2one('product.product', related='order_line.product_id', string='Product')
    sale_id = fields.Many2one('sale.order', string='SO Reference')
